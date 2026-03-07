"""
execution_handler.py

Simulates trade execution.
"""

from core.event import FillEvent

class ExecutionHandler:
    """
    Receives OrderEvent and generates FillEvent.
    """

    def execute_order(self, order_event, current_price=None):
        """
        Simulate immediate fill at market price.
        
        Parameters:
        -----------
        order_event : OrderEvent
            The order to execute
        current_price : float, optional
            Current market price. If None, uses order price
            
        Returns:
        --------
        FillEvent
            The fill event from the simulated execution
        """
        fill_price = current_price if current_price is not None else order_event.price
        
        # Use timestamp from order if available, otherwise None
        timestamp = getattr(order_event, 'timestamp', None)
        
        fill = FillEvent(
            symbol=order_event.symbol,
            fill_type=order_event.order_type,
            quantity=order_event.quantity,
            price=fill_price,
            timestamp=timestamp
        )
        return fill