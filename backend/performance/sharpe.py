"""Sharpe Ratio and risk-adjusted return calculations."""

from typing import List
import math


class SharpeCalculator:
    """Calculate Sharpe Ratio and related metrics."""
    
    @staticmethod
    def calculate_returns(equity_curve: List[float]) -> List[float]:
        """Calculate returns from equity curve.
        
        Args:
            equity_curve: List of portfolio values
            
        Returns:
            List of returns (percentage changes)
        """
        returns = []
        for i in range(1, len(equity_curve)):
            if equity_curve[i-1] != 0:
                ret = (equity_curve[i] - equity_curve[i-1]) / equity_curve[i-1]
            else:
                ret = 0.0
            returns.append(ret)
        
        return returns
    
    @staticmethod
    def calculate_sharpe_ratio(returns: List[float], periods_per_year: int = 252, 
                              risk_free_rate: float = 0.02) -> float:
        """Calculate Sharpe Ratio.
        
        Args:
            returns: List of returns
            periods_per_year: Trading periods per year (252 for daily)
            risk_free_rate: Annual risk-free rate
            
        Returns:
            Sharpe Ratio
        """
        if not returns or len(returns) < 2:
            return 0.0
        
        excess_returns = [r - (risk_free_rate / periods_per_year) for r in returns]
        
        mean_excess = sum(excess_returns) / len(excess_returns)
        variance = sum((r - mean_excess) ** 2 for r in excess_returns) / len(excess_returns)
        std_dev = math.sqrt(variance) if variance > 0 else 0
        
        if std_dev == 0:
            return 0.0
        
        sharpe = (mean_excess * periods_per_year) / (std_dev * math.sqrt(periods_per_year))
        return sharpe
    
    @staticmethod
    def calculate_sortino_ratio(returns: List[float], periods_per_year: int = 252,
                               risk_free_rate: float = 0.02, target_return: float = 0.0) -> float:
        """Calculate Sortino Ratio (only considers downside volatility).
        
        Args:
            returns: List of returns
            periods_per_year: Trading periods per year
            risk_free_rate: Annual risk-free rate
            target_return: Target return (default 0)
            
        Returns:
            Sortino Ratio
        """
        if not returns or len(returns) < 2:
            return 0.0
        
        excess_returns = [r - (risk_free_rate / periods_per_year) for r in returns]
        mean_excess = sum(excess_returns) / len(excess_returns)
        
        # Only downside volatility
        downside_returns = [r - target_return for r in excess_returns if r < target_return]
        
        if not downside_returns:
            return float('inf') if mean_excess > 0 else 0.0
        
        downside_variance = sum(r ** 2 for r in downside_returns) / len(excess_returns)
        downside_std = math.sqrt(downside_variance) if downside_variance > 0 else 0
        
        if downside_std == 0:
            return float('inf') if mean_excess > 0 else 0.0
        
        sortino = (mean_excess * periods_per_year) / (downside_std * math.sqrt(periods_per_year))
        return sortino
    
    @staticmethod
    def calculate_calmar_ratio(returns: List[float], max_drawdown: float, 
                              periods_per_year: int = 252) -> float:
        """Calculate Calmar Ratio (return / max drawdown).
        
        Args:
            returns: List of returns
            max_drawdown: Maximum drawdown (as decimal)
            periods_per_year: Trading periods per year
            
        Returns:
            Calmar Ratio
        """
        if max_drawdown == 0:
            return 0.0
        
        total_return = (1 + returns[0]) ** len(returns) - 1 if returns else 0
        years = len(returns) / periods_per_year if returns else 0
        annual_return = (total_return / years) if years > 0 else 0
        
        return annual_return / max_drawdown
    
    @staticmethod
    def calculate_volatility(returns: List[float], periods_per_year: int = 252) -> float:
        """Calculate annualized volatility.
        
        Args:
            returns: List of returns
            periods_per_year: Trading periods per year
            
        Returns:
            Annualized volatility
        """
        if not returns or len(returns) < 2:
            return 0.0
        
        mean_return = sum(returns) / len(returns)
        variance = sum((r - mean_return) ** 2 for r in returns) / len(returns)
        daily_volatility = math.sqrt(variance) if variance > 0 else 0
        
        return daily_volatility * math.sqrt(periods_per_year)
