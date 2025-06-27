from config.config_loader import load_config
from data.data_loader import get_price_volume_data
from data.etf_universe import construct_universe
from signals.alpha_signal import compute_signals
from portfolio.optimizer import optimize_portfolio
from execution.rebalance import simulate_rebalance
from attribution.performance_analysis import analyze_performance
from utils.plot import plot_cumulative_returns
import pandas as pd
import yfinance as yf

def main():
    # Step 1: Load config
    config = load_config("config/config.yaml")

    # Step 2: Define ETF universe
    universe = construct_universe(config)  # returns List[str]

    # Step 3: Download historical price data
    price_data = get_price_volume_data(universe, config)  # pd.DataFrame: index=date, columns=tickers

    # Step 4: Generate alpha signals
    alpha_signal = compute_signals(price_data, config)  # pd.Series: expected returns

    # Step 5: Optimize portfolio weights
    weights = optimize_portfolio(expected_returns=alpha_signal,
                                 price_data=price_data,
                                 min_risk=config.get("min_risk", 0.03),
                                 long_only=config.get("long_only", True))  # pd.Series

    # Step 6: Simulate execution with T+1 logic
    simulated_returns = simulate_rebalance(
        weights_df = pd.DataFrame([weights.values] * len(price_data), 
        columns=weights.index, 
        index=price_data.index),
        price_df=price_data)

    # Step 7: Analyze portfolio performance with attribution and hedging
    # Market factor: SPY
    spy = yf.download("SPY", start=price_data.index[0], end=price_data.index[-1])["Close"].pct_change()
    spy.name = "SPY"
    factor_df = pd.DataFrame(spy).reindex(simulated_returns.index).dropna()

    # Hedging asset: TLT
    # ✅ Make sure tlt is a Series
    # In main.py, ensure hedge_returns is a Series
    tlt = yf.download("TLT", start=price_data.index[0], end=price_data.index[-1])["Close"].pct_change()
    tlt = tlt.reindex(simulated_returns.index).shift(1).fillna(0)
    tlt.name = "hedge"
    hedge_returns = tlt.squeeze()

    print(f"simulated_returns.index.head():\n{simulated_returns.index[:5]}")
    print(f"hedge_returns.index.head():\n{hedge_returns.index[:5]}")
    print(f"Combined.head():\n{(simulated_returns + hedge_returns).head()}")


    # Attribution: performance, beta exposure, and hedging
    analyze_performance(simulated_returns, factor_df=factor_df, hedge_returns=hedge_returns)

    # Step 8: Visualize results
    plot_cumulative_returns(simulated_returns)

if __name__ == "__main__":
    main()
