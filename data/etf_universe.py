import yfinance as yf
import pandas as pd

# Keywords that indicate leveraged or inverse ETFs
EXCLUDE_KEYWORDS = ['3x', '2x', 'leveraged', 'ultra', 'inverse', 'bear', 'short', 'daily']

def is_leveraged_or_inverse(name: str) -> bool:
    """
    Check if the ETF name suggests it is leveraged or inverse.
    """
    name = name.lower()
    return any(keyword in name for keyword in EXCLUDE_KEYWORDS)

def construct_etf_universe(etf_list: list[str], min_avg_volume: int = 1_000_000) -> pd.DataFrame:
    """
    Build the ETF universe by filtering out leveraged/inverse products and low-liquidity ETFs.

    Args:
        etf_list (list): List of ETF tickers.
        min_avg_volume (int): Minimum average daily volume threshold.

    Returns:
        pd.DataFrame: Filtered list of valid ETFs with metadata.
    """
    filtered = []

    for ticker in etf_list:
        try:
            info = yf.Ticker(ticker).info
            long_name = info.get("longName", "")
            avg_volume = info.get("averageVolume", 0)
            category = info.get("category", "")
            region = info.get("region", "Unknown")

            if is_leveraged_or_inverse(long_name):
                print(f"⛔️ Excluded {ticker}: suspected leveraged/inverse ETF.")
                continue
            if avg_volume < min_avg_volume:
                print(f"⚠️ Excluded {ticker}: low average volume = {avg_volume}")
                continue

            filtered.append({
                "ticker": ticker,
                "name": long_name,
                "avg_volume": avg_volume,
                "category": category,
                "region": region
            })

        except Exception as e:
            print(f"❌ Failed to fetch {ticker}: {e}")
            continue

    return pd.DataFrame(filtered)

def construct_universe(config: dict) -> list[str]:
    """
    Wrapper to construct ETF universe using tickers from config.
    """
    etf_list = config.get("etfs", [])
    df = construct_etf_universe(etf_list)
    return df["ticker"].tolist()

if __name__ == "__main__":
    # Example ticker list; should be loaded from config in production
    etfs = ['SPY', 'QQQ', 'VTI', 'IWM', 'ARKK', 'TQQQ', 'SH', 'XLK', 'EFA', 'EEM']
    universe_df = construct_etf_universe(etfs)
    print("\n✅ Final ETF Universe:")
    print(universe_df)
