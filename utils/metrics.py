import numpy as np
import pandas as pd

def annualized_return(returns: pd.Series) -> float:
    return returns.mean() * 252

def annualized_volatility(returns: pd.Series) -> float:
    return returns.std() * np.sqrt(252)

def sharpe_ratio(returns: pd.Series, risk_free_rate: float = 0.0) -> float:
    excess_returns = returns - risk_free_rate / 252
    vol = annualized_volatility(excess_returns)
    if vol == 0:
        return np.nan
    return annualized_return(excess_returns) / vol
