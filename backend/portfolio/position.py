"""Position management for portfolio."""

from dataclasses import dataclass


@dataclass
class Position:
    """Represents a position in a security."""
    symbol: str
    quantity: int = 0
    avg_price: float = 0.0
    
    def update(self, quantity: int, price: float) -> None:
        """Update position with new trade."""
        if self.quantity == 0:
            self.avg_price = price
        else:
            # Calculate new average price
            total_value = (self.quantity * self.avg_price) + (quantity * price)
            self.quantity += quantity
            if self.quantity != 0:
                self.avg_price = total_value / self.quantity
            else:
                self.avg_price = 0.0
        
        # Ensure quantity doesn't go negative (simplified)
        if self.quantity < 0:
            self.quantity = 0
            self.avg_price = 0.0
    
    def get_value(self, current_price: float) -> float:
        """Get current position value."""
        return self.quantity * current_price
