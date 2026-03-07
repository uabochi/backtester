"""
sma_strategy.py

Example strategy: Simple Moving Average (SMA) Crossover
"""

from strategy.base_strategy import Strategy

class SMA_Crossover_Strategy(Strategy):
    """
    Simple Moving Average crossover strategy:
    - BUY when short SMA crosses above long SMA
    - SELL when short SMA crosses below long SMA
    """

    def __init__(self, symbol, data_handler, event_queue, short_window=5, long_window=20):
        super().__init__(symbol, data_handler, event_queue)
        self.short_window = short_window
        self.long_window = long_window
        self.in_position = False

    def on_market_event(self, market_event):
        history = self.data_handler.get_latest_bars(self.long_window)
        if len(history) < self.long_window:
            return  # Not enough data

        short_sma = history["close"].tail(self.short_window).mean()
        long_sma = history["close"].tail(self.long_window).mean()

        if short_sma > long_sma and not self.in_position:
            self.generate_signal("BUY")
            self.in_position = True
        elif short_sma < long_sma and self.in_position:
            self.generate_signal("SELL")
            self.in_position = False
        else:
            self.generate_signal("HOLD")