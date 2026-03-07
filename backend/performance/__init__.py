"""Performance metrics and analysis."""

from .metrics import (
    generate_equity_curve,
    calculate_win_rate,
    calculate_max_drawdown,
    calculate_sharpe_ratio,
    trade_statistics
)
from .visualization import plot_equity_curve, plot_trades

__all__ = [
    'generate_equity_curve',
    'calculate_win_rate',
    'calculate_max_drawdown',
    'calculate_sharpe_ratio',
    'trade_statistics',
    'plot_equity_curve',
    'plot_trades'
]
