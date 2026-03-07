"""
portfolio.py

Tracks open positions, account equity, stop-loss/take-profit, and logs trades.
"""

import pandas as pd
from core.event import OrderEvent

class Portfolio:
    """
    Portfolio manager for event-driven engine.
    """

    def __init__(self, initial_cash=10000):
        self.cash = initial_cash
        self.equity = initial_cash
        self.positions = {}  # symbol -> position dict
        self.trade_log = []

    def update_signal(self, signal_event):
        """
        Convert signal into OrderEvent.
        """
        symbol = signal_event.symbol
        signal_type = signal_event.signal_type
        timestamp = signal_event.timestamp

        if signal_type == "BUY":
            order = OrderEvent(symbol, "BUY", quantity=1, timestamp=timestamp)
            return order
        elif signal_type == "SELL":
            order = OrderEvent(symbol, "SELL", quantity=1, timestamp=timestamp)
            return order
        else:
            return None

    def update_fill(self, fill_event):
        """
        Update positions, equity, and log trade.
        """
        symbol = fill_event.symbol
        qty = fill_event.quantity
        price = fill_event.price
        timestamp = fill_event.timestamp
        fill_type = fill_event.fill_type

        # Update position
        if symbol not in self.positions:
            self.positions[symbol] = {"quantity": 0, "avg_price": 0}

        pos = self.positions[symbol]

        if fill_type == "BUY":
            total_cost = pos["avg_price"] * pos["quantity"] + price * qty
            pos["quantity"] += qty
            pos["avg_price"] = total_cost / pos["quantity"]
            self.cash -= price * qty
        elif fill_type == "SELL":
            self.cash += price * qty
            pos["quantity"] -= qty
            if pos["quantity"] == 0:
                pos["avg_price"] = 0

        # Update equity
        self.equity = self.cash + sum(
            p["quantity"] * p["avg_price"] for p in self.positions.values()
        )

        # Log trade
        self.trade_log.append({
            "symbol": symbol,
            "type": fill_type,
            "quantity": qty,
            "price": price,
            "timestamp": timestamp,
            "cash": self.cash,
            "equity": self.equity
        })