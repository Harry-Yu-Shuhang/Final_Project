import numpy as np
import pandas as pd
from scipy.optimize import minimize

def annualized_volatility(weights, cov_matrix):
    daily_var = np.dot(weights.T, np.dot(cov_matrix, weights))
    return np.sqrt(daily_var) * np.sqrt(252)

def sharpe_ratio(weights, expected_returns, cov_matrix, risk_free_rate=0.0):
    excess_returns = expected_returns - risk_free_rate
    port_return = np.dot(weights, excess_returns)
    port_vol = annualized_volatility(weights, cov_matrix)
    return -port_return / port_vol  # negative for minimization

def optimize_portfolio(expected_returns: pd.Series, price_data: pd.DataFrame, 
                       min_risk: float = 0.03, long_only: bool = True) -> pd.Series:
    """
    Optimize portfolio weights to maximize Sharpe Ratio with constraints.

    Args:
        expected_returns (pd.Series): Alpha signal or expected return per ETF.
        price_data (pd.DataFrame): Historical price for covariance estimation.
        min_risk (float): Minimum portfolio volatility (annualized).
        long_only (bool): If True, only allow long positions.

    Returns:
        pd.Series: Optimized portfolio weights.
    """
    tickers = expected_returns.index.tolist()
    returns = price_data.pct_change().dropna()
    cov_matrix = returns.cov().values

    n = len(tickers)
    init_weights = np.ones(n) / n

    # Constraints:
    constraints = [
        {'type': 'ineq', 'fun': lambda w: annualized_volatility(w, cov_matrix) - min_risk},  # min volatility
        {'type': 'ineq', 'fun': lambda w: 1.0 - np.sum(np.abs(w))}  # L1-norm budget
    ]

    bounds = [(0, 1)] * n if long_only else [(-1, 1)] * n

    result = minimize(sharpe_ratio,
                      x0=init_weights,
                      args=(expected_returns.values, cov_matrix),
                      method='SLSQP',
                      bounds=bounds,
                      constraints=constraints)

    if not result.success:
        raise ValueError(f"Optimization failed: {result.message}")

    return pd.Series(result.x, index=tickers)
