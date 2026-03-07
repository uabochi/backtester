"""Trade logging and history."""

from typing import List, Dict, Optional
from datetime import datetime
from dataclasses import dataclass


@dataclass
class Trade:
    """Represents a completed trade."""
    entry_time: datetime
    exit_time: Optional[datetime]
    symbol: str
    direction: str  # BUY or SELL
    quantity: int
    entry_price: float
    exit_price: Optional[float]
    commission: float
    profit_loss: Optional[float] = None
    profit_loss_pct: Optional[float] = None
    
    def close_trade(self, exit_price: float, exit_time: datetime, commission: float):
        """Close the trade."""
        self.exit_price = exit_price
        self.exit_time = exit_time
        self.commission += commission
        
        # Calculate P&L
        if self.direction == 'BUY':
            self.profit_loss = (exit_price - self.entry_price) * self.quantity - self.commission
        else:  # SELL
            self.profit_loss = (self.entry_price - exit_price) * self.quantity - self.commission
        
        entry_value = self.entry_price * self.quantity
        if entry_value > 0:
            self.profit_loss_pct = self.profit_loss / entry_value


class TradeLogger:
    """Log and track trades."""
    
    def __init__(self):
        """Initialize trade logger."""
        self.trades: List[Trade] = []
        self.open_trades: Dict[str, Trade] = {}
    
    def open_trade(self, entry_time: datetime, symbol: str, direction: str, 
                   quantity: int, entry_price: float, commission: float) -> Trade:
        """Open a new trade."""
        trade = Trade(
            entry_time=entry_time,
            exit_time=None,
            symbol=symbol,
            direction=direction,
            quantity=quantity,
            entry_price=entry_price,
            exit_price=None,
            commission=commission
        )
        self.open_trades[symbol] = trade
        return trade
    
    def close_trade(self, exit_time: datetime, symbol: str, 
                   exit_price: float, commission: float) -> Optional[Trade]:
        """Close an open trade."""
        if symbol not in self.open_trades:
            return None
        
        trade = self.open_trades[symbol]
        trade.close_trade(exit_price, exit_time, commission)
        self.trades.append(trade)
        del self.open_trades[symbol]
        return trade
    
    def get_trade_history(self) -> List[Trade]:
        """Get all completed trades."""
        return self.trades.copy()
    
    def get_stats(self) -> Dict:
        """Calculate trade statistics."""
        if not self.trades:
            return {}
        
        winning_trades = [t for t in self.trades if t.profit_loss and t.profit_loss > 0]
        losing_trades = [t for t in self.trades if t.profit_loss and t.profit_loss <= 0]
        
        total_profit = sum(t.profit_loss for t in self.trades if t.profit_loss)
        total_trades = len(self.trades)
        win_rate = len(winning_trades) / total_trades if total_trades > 0 else 0
        
        return {
            'total_trades': total_trades,
            'winning_trades': len(winning_trades),
            'losing_trades': len(losing_trades),
            'win_rate': win_rate,
            'total_profit': total_profit,
            'avg_profit_per_trade': total_profit / total_trades if total_trades > 0 else 0
        }
