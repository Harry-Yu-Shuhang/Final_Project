import pandas as pd

def simulate_rebalance(weights_df: pd.DataFrame, price_df: pd.DataFrame) -> pd.Series:
    """
    Simulate portfolio returns under T+1 execution lag logic.

    Args:
        weights_df (pd.DataFrame): Portfolio weights indexed by date T (rebalance signal date).
                                   Should be aligned with price_df index.
        price_df (pd.DataFrame): Adjusted close prices of ETFs.

    Returns:
        pd.Series: Portfolio returns under T+1 execution.
    """
    returns = price_df.pct_change().shift(-1)  # return from T+1 to T+2
    returns = returns.loc[weights_df.index]    # align with rebalance signal dates

    # Simulate return: weights from T → executed at close T+1 → realized return from T+1 to T+2
    port_returns = (weights_df.shift(1) * returns).sum(axis=1)
    return port_returns.dropna()