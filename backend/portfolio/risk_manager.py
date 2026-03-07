"""Risk management."""

from typing import Optional


class RiskManager:
    """Risk management and position sizing."""
    
    def __init__(self, 
                 max_position_size: float = 0.1,
                 max_loss_pct: float = 0.02,
                 stop_loss_pct: float = 0.05):
        """Initialize risk manager.
        
        Args:
            max_position_size: Max position as % of portfolio (0.1 = 10%)
            max_loss_pct: Max loss allowed per trade as % of portfolio
            stop_loss_pct: Default stop loss % below entry
        """
        self.max_position_size = max_position_size
        self.max_loss_pct = max_loss_pct
        self.stop_loss_pct = stop_loss_pct
    
    def calculate_position_size(self, 
                               portfolio_value: float,
                               entry_price: float,
                               stop_loss_price: float) -> int:
        """Calculate position size based on risk.
        
        Args:
            portfolio_value: Current portfolio value
            entry_price: Entry price
            stop_loss_price: Stop loss price
            
        Returns:
            Position size in units
        """
        # Max position size
        max_allocation = portfolio_value * self.max_position_size
        
        # Risk-based sizing
        risk_per_unit = abs(entry_price - stop_loss_price)
        max_risk = portfolio_value * self.max_loss_pct
        
        if risk_per_unit > 0:
            risk_based_size = max_risk / risk_per_unit
        else:
            risk_based_size = max_allocation / entry_price
        
        # Take the more conservative size
        position_value = min(max_allocation, risk_based_size)
        position_size = int(position_value / entry_price)
        
        return max(position_size, 0)
    
    def calculate_stop_loss(self, entry_price: float, direction: str = 'BUY') -> float:
        """Calculate stop loss price.
        
        Args:
            entry_price: Entry price
            direction: 'BUY' or 'SELL'
            
        Returns:
            Stop loss price
        """
        if direction == 'BUY':
            return entry_price * (1 - self.stop_loss_pct)
        else:  # SELL
            return entry_price * (1 + self.stop_loss_pct)
    
    def should_close_position(self, 
                             current_price: float,
                             entry_price: float,
                             stop_loss_price: float) -> bool:
        """Check if position should be closed (hit stop loss).
        
        Args:
            current_price: Current price
            entry_price: Entry price
            stop_loss_price: Stop loss price
            
        Returns:
            True if stop loss hit
        """
        return ((entry_price > stop_loss_price and current_price <= stop_loss_price) or
                (entry_price < stop_loss_price and current_price >= stop_loss_price))
