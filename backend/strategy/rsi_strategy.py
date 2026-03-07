"""
rsi_strategy.py

Template for RSI-based strategy.
"""

from strategy.base_strategy import Strategy

class RSI_Strategy(Strategy):
    """
    Placeholder RSI strategy:
    - Buy when RSI < 30
    - Sell when RSI > 70
    """

    def __init__(self, symbol, data_handler, event_queue, period=14, overbought=70, oversold=30):
        super().__init__(symbol, data_handler, event_queue)
        self.period = period
        self.overbought = overbought
        self.oversold = oversold
        self.in_position = False

    def on_market_event(self, market_event):
        history = self.data_handler.get_latest_bars(self.period + 1)
        if len(history) < self.period:
            return

        delta = history["close"].diff()
        gain = delta.clip(lower=0).tail(self.period).mean()
        loss = -delta.clip(upper=0).tail(self.period).mean()
        rsi = 100 - (100 / (1 + gain / (loss + 1e-6)))

        if rsi < self.oversold and not self.in_position:
            self.generate_signal("BUY")
            self.in_position = True
        elif rsi > self.overbought and self.in_position:
            self.generate_signal("SELL")
            self.in_position = False
        else:
            self.generate_signal("HOLD")