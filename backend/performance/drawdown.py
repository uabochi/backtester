"""Drawdown calculation module."""

from typing import List, Tuple, Dict


class DrawdownCalculator:
    """Calculate drawdown metrics."""
    
    @staticmethod
    def calculate_running_max(equity_curve: List[float]) -> List[float]:
        """Calculate running maximum of equity curve.
        
        Args:
            equity_curve: List of portfolio values over time
            
        Returns:
            List of running maximum values
        """
        running_max = []
        current_max = equity_curve[0]
        
        for value in equity_curve:
            if value > current_max:
                current_max = value
            running_max.append(current_max)
        
        return running_max
    
    @staticmethod
    def calculate_drawdown_series(equity_curve: List[float]) -> List[float]:
        """Calculate drawdown at each point.
        
        Args:
            equity_curve: List of portfolio values over time
            
        Returns:
            List of drawdown percentages
        """
        running_max = DrawdownCalculator.calculate_running_max(equity_curve)
        
        drawdowns = []
        for i, value in enumerate(equity_curve):
            if running_max[i] != 0:
                dd = (running_max[i] - value) / running_max[i]
            else:
                dd = 0.0
            drawdowns.append(dd)
        
        return drawdowns
    
    @staticmethod
    def calculate_max_drawdown(equity_curve: List[float]) -> float:
        """Calculate maximum drawdown.
        
        Args:
            equity_curve: List of portfolio values
            
        Returns:
            Maximum drawdown as percentage (0-1)
        """
        if not equity_curve or len(equity_curve) < 2:
            return 0.0
        
        drawdowns = DrawdownCalculator.calculate_drawdown_series(equity_curve)
        return max(drawdowns) if drawdowns else 0.0
    
    @staticmethod
    def calculate_drawdown_duration(equity_curve: List[float]) -> Tuple[int, float]:
        """Calculate longest drawdown duration and depth.
        
        Args:
            equity_curve: List of portfolio values
            
        Returns:
            Tuple of (duration_in_periods, max_depth)
        """
        running_max = DrawdownCalculator.calculate_running_max(equity_curve)
        
        max_duration = 0
        current_duration = 0
        max_depth = 0.0
        
        for i, value in enumerate(equity_curve):
            if running_max[i] != 0:
                dd = (running_max[i] - value) / running_max[i]
            else:
                dd = 0.0
            
            if dd > 0:
                current_duration += 1
                max_depth = max(max_depth, dd)
                max_duration = max(max_duration, current_duration)
            else:
                current_duration = 0
                max_depth = 0.0
        
        return (max_duration, max_depth)
    
    @staticmethod
    def calculate_recovery_time(equity_curve: List[float]) -> Dict:
        """Calculate recovery time from drawdowns.
        
        Args:
            equity_curve: List of portfolio values
            
        Returns:
            Dictionary with recovery metrics
        """
        running_max = DrawdownCalculator.calculate_running_max(equity_curve)
        
        recovery_times = []
        in_drawdown = False
        drawdown_start = 0
        peak_value = equity_curve[0]
        
        for i, value in enumerate(equity_curve):
            if value >= running_max[i-1] if i > 0 else value >= equity_curve[0]:
                if in_drawdown:
                    recovery_times.append(i - drawdown_start)
                    in_drawdown = False
            elif running_max[i] > peak_value:
                peak_value = running_max[i]
                if not in_drawdown:
                    drawdown_start = i
                    in_drawdown = True
        
        return {
            'recovery_times': recovery_times,
            'average_recovery': sum(recovery_times) / len(recovery_times) if recovery_times else 0,
            'max_recovery_time': max(recovery_times) if recovery_times else 0,
        }
