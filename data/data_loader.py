import yfinance as yf
import pandas as pd
from typing import List, Dict

def get_price_volume_data(tickers: List[str], config: Dict) -> pd.DataFrame:
    """
    Download adjusted close price and volume data for given tickers.

    Args:
        tickers (List[str]): List of ETF symbols.
        config (Dict): Configuration with 'start_date' and 'end_date'.

    Returns:
        pd.DataFrame: Multi-index DataFrame with ('Date', 'Ticker') and columns ['Close', 'Volume']
    """
    start_date = config.get("start_date", "2015-01-01")
    end_date = config.get("end_date", None)

    # Download data using yfinance
    print(f"📥 Downloading data for {tickers} from {start_date} to {end_date}")
    raw_data = yf.download(tickers=tickers, start=start_date, end=end_date, group_by="ticker", auto_adjust=True)

    # Extract and clean adjusted close & volume
    price_df = pd.DataFrame()
    volume_df = pd.DataFrame()

    for ticker in tickers:
        df = raw_data[ticker][["Close", "Volume"]].copy()
        df.columns = [ticker + "_price", ticker + "_volume"]
        price_df[ticker] = df[ticker + "_price"]
        volume_df[ticker] = df[ticker + "_volume"]

    # Align and drop missing values
    price_df = price_df.dropna(how="any")
    volume_df = volume_df.reindex(price_df.index)

    print(f"✅ Final price data shape: {price_df.shape}")
    return price_df
