"""
base_strategy.py

Abstract base class for all trading strategies.
All strategies must inherit from this class and implement on_market_event().
"""

from abc import ABC, abstractmethod
from core.event import SignalEvent

class Strategy(ABC):
    """
    Base class for event-driven trading strategies.
    """

    def __init__(self, symbol, data_handler, event_queue):
        self.symbol = symbol
        self.data_handler = data_handler
        self.event_queue = event_queue
        self.signals = []

    @abstractmethod
    def on_market_event(self, market_event):
        """
        Process a market event and generate signals.
        Must be implemented by child strategy classes.
        """
        pass

    def generate_signal(self, signal_type: str):
        """
        Push a signal to the event queue.
        """
        timestamp = self.data_handler.get_latest_bars(1)["timestamp"].iloc[-1]
        signal_event = SignalEvent(self.symbol, signal_type, timestamp)
        self.signals.append(signal_event)
        self.event_queue.put(signal_event)