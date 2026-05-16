"""Data provider plugins."""

from trading_agent_os.data.csv_market import CsvMarketDataProvider
from trading_agent_os.data.synthetic import SyntheticMarketDataProvider

__all__ = ["CsvMarketDataProvider", "SyntheticMarketDataProvider"]
