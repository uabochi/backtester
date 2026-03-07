"""
data.py

Data ingestion module for the event-driven backtesting engine.

Responsibilities:
- Load OHLCV historical data from CSV
- Validate data integrity
- Ensure chronological ordering
- Provide sequential bar-by-bar access for the engine
"""

import pandas as pd


class DataHandler:
    """
    Handles loading and streaming historical market data.

    The backtesting engine should not access the entire dataset directly.
    Instead, it requests one bar at a time to prevent lookahead bias.
    """

    REQUIRED_COLUMNS = ["timestamp", "open", "high", "low", "close", "volume"]

    def __init__(self, csv_path: str):
        """
        Initialize the data handler.

        Parameters
        ----------
        csv_path : str
            Path to the OHLCV CSV file.
        """
        self.csv_path = csv_path
        self.data = None
        self.current_index = 0

        # Load and validate dataset
        self._load_csv()
        self._validate_data()
        self._prepare_data()

    def _load_csv(self):
        """
        Load CSV data into a pandas DataFrame.
        """
        try:
            self.data = pd.read_csv(self.csv_path)
        except Exception as e:
            raise RuntimeError(f"Error loading CSV file: {e}")

    def _validate_data(self):
        """
        Validate that the dataset contains the required columns
        and has no missing values in critical fields.
        """

        # Check required columns exist
        missing_cols = [
            col for col in self.REQUIRED_COLUMNS if col not in self.data.columns
        ]

        if missing_cols:
            raise ValueError(f"CSV missing required columns: {missing_cols}")

        # Check for missing values
        if self.data[self.REQUIRED_COLUMNS].isnull().any().any():
            raise ValueError("Dataset contains missing OHLCV values.")

    def _prepare_data(self):
        """
        Prepare data for use in the backtester.

        Steps:
        1. Convert timestamps to datetime
        2. Sort chronologically
        3. Reset index
        """

        # Convert timestamp column to datetime
        self.data["timestamp"] = pd.to_datetime(self.data["timestamp"])

        # Ensure chronological ordering
        self.data = self.data.sort_values("timestamp")

        # Reset index for clean sequential iteration
        self.data = self.data.reset_index(drop=True)

    def has_next(self) -> bool:
        """
        Check whether more bars are available.

        Returns
        -------
        bool
        """
        return self.current_index < len(self.data)

    def get_next_bar(self) -> dict:
        """
        Return the next OHLCV bar for the engine.

        This method simulates live market data by returning
        one bar at a time.

        Returns
        -------
        dict
            {
                "timestamp": datetime,
                "open": float,
                "high": float,
                "low": float,
                "close": float,
                "volume": float
            }
        """

        if not self.has_next():
            raise StopIteration("No more data available.")

        row = self.data.iloc[self.current_index]
        self.current_index += 1

        # Convert row to dictionary format
        bar = {
            "timestamp": row["timestamp"],
            "open": row["open"],
            "high": row["high"],
            "low": row["low"],
            "close": row["close"],
            "volume": row["volume"],
        }

        return bar

    def reset(self):
        """
        Reset data iteration to the beginning.

        Useful for running multiple backtests
        without reloading the CSV.
        """
        self.current_index = 0

    def get_latest_bars(self, lookback: int):
        """
        Return a slice of historical bars for indicator calculations.

        Parameters
        ----------
        lookback : int
            Number of previous bars required.

        Returns
        -------
        pandas.DataFrame
        """

        if self.current_index < lookback:
            return self.data.iloc[:self.current_index]

        return self.data.iloc[self.current_index - lookback : self.current_index]