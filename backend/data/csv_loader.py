"""CSV data loader for backtester."""

import pandas as pd
from pathlib import Path
from typing import Optional


class CSVLoader:
    """Load OHLCV data from CSV files."""
    
    def __init__(self, filepath: str):
        """Initialize CSV loader with file path."""
        self.filepath = Path(filepath)
    
    def load(self) -> pd.DataFrame:
        """Load CSV data and return DataFrame.
        
        Expected columns: Date, Open, High, Low, Close, Volume
        """
        df = pd.read_csv(self.filepath)
        df['Date'] = pd.to_datetime(df['Date'])
        df.set_index('Date', inplace=True)
        return df
    
    def validate(self, df: pd.DataFrame) -> bool:
        """Validate OHLCV data structure."""
        required_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
        return all(col in df.columns for col in required_cols)
