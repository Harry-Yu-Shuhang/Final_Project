import pandas as pd

def compute_trend_signal(price_data: pd.DataFrame, short_window: int = 20, long_window: int = 100) -> pd.Series:
    """
    Generate a trend-following alpha signal based on moving average crossover.

    Args:
        price_data (pd.DataFrame): DataFrame with datetime index and one column per ETF (adjusted close).
        short_window (int): Window size for short-term moving average.
        long_window (int): Window size for long-term moving average.

    Returns:
        pd.Series: Cross-sectional alpha signal for each ETF at the last date.
                   Positive value indicates bullish trend, negative indicates bearish.
    """
    short_ma = price_data.rolling(window=short_window).mean()
    long_ma = price_data.rolling(window=long_window).mean()

    signal = short_ma - long_ma
    latest_signal = signal.iloc[-1]  # Use the most recent cross-sectional signal
    return latest_signal


def compute_signals(price_data: pd.DataFrame, config: dict) -> pd.Series:
    """
    Wrapper for alpha signal computation. You can switch signal logic via config.
    """
    return compute_trend_signal(price_data)
