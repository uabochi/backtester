"""
event.py

Defines all event types for the event-driven backtesting engine.
"""

class Event:
    """Base class for all events."""
    pass

class MarketEvent(Event):
    """Signals a new market data bar is available."""
    def __init__(self, bar):
        self.type = "MARKET"
        self.bar = bar  # dictionary with OHLCV data

class SignalEvent(Event):
    """Signals that a strategy wants to enter or exit a position."""
    def __init__(self, symbol, signal_type, timestamp):
        self.type = "SIGNAL"
        self.symbol = symbol
        self.signal_type = signal_type  # 'BUY', 'SELL', 'HOLD'
        self.timestamp = timestamp

class OrderEvent(Event):
    """Signals that a portfolio wants to execute a trade."""
    def __init__(self, symbol, order_type, quantity, price=None, timestamp=None):
        self.type = "ORDER"
        self.symbol = symbol
        self.order_type = order_type  # 'BUY' or 'SELL'
        self.quantity = quantity
        self.price = price  # optional, simulated market price
        self.timestamp = timestamp  # carries forward from signal

class FillEvent(Event):
    """Signals that an order has been executed."""
    def __init__(self, symbol, fill_type, quantity, price, timestamp):
        self.type = "FILL"
        self.symbol = symbol
        self.fill_type = fill_type  # 'BUY' or 'SELL'
        self.quantity = quantity
        self.price = price
        self.timestamp = timestamp