"""
metrics.py

Calculates performance metrics for backtesting:
- Win rate
- Maximum drawdown
- Sharpe ratio
- Equity curve generation
- Trade statistics summary
"""

import pandas as pd
import numpy as np


def generate_equity_curve(trade_log):
    """
    Generates an equity curve from trade log.

    Parameters
    ----------
    trade_log : list of dict
        Each dict should have 'timestamp' and 'equity' keys.

    Returns
    -------
    pd.DataFrame
        DataFrame with timestamp and equity over time.
    """
    if not trade_log:
        return pd.DataFrame(columns=["timestamp", "equity"])
    
    df = pd.DataFrame(trade_log)
    df = df.sort_values("timestamp").reset_index(drop=True)
    return df[["timestamp", "equity"]]


def calculate_win_rate(trade_log):
    """
    Calculates the percentage of winning trades.

    Parameters
    ----------
    trade_log : list of dict
        Each dict should have 'type' ('BUY'/'SELL'), 'price', 'quantity'

    Returns
    -------
    float
        Win rate as a percentage
    """
    df = pd.DataFrame(trade_log)
    if df.empty or "type" not in df.columns or "price" not in df.columns:
        return 0.0

    # Only consider closed trades (BUY then SELL)
    trades = []
    position = {}
    for i, row in df.iterrows():
        sym = row["symbol"]
        if sym not in position:
            position[sym] = {"qty": 0, "entry_price": 0}

        if row["type"] == "BUY":
            # Enter position
            position[sym]["qty"] += row["quantity"]
            position[sym]["entry_price"] = row["price"]
        elif row["type"] == "SELL" and position[sym]["qty"] > 0:
            profit = (row["price"] - position[sym]["entry_price"]) * position[sym]["qty"]
            trades.append(profit)
            position[sym]["qty"] = 0
            position[sym]["entry_price"] = 0

    if len(trades) == 0:
        return 0.0

    wins = [t for t in trades if t > 0]
    return len(wins) / len(trades) * 100


def calculate_max_drawdown(equity_curve):
    """
    Calculates the maximum drawdown from equity curve.

    Parameters
    ----------
    equity_curve : pd.DataFrame
        DataFrame with 'equity' column

    Returns
    -------
    float
        Maximum drawdown as a percentage
    """
    equity = equity_curve["equity"]
    roll_max = equity.cummax()
    drawdown = (equity - roll_max) / roll_max
    return drawdown.min() * 100  # negative percentage


def calculate_sharpe_ratio(equity_curve, risk_free_rate=0.0, periods_per_year=252):
    """
    Calculates annualized Sharpe ratio.

    Parameters
    ----------
    equity_curve : pd.DataFrame
        DataFrame with 'equity' column
    risk_free_rate : float
        Risk-free rate per period
    periods_per_year : int
        Number of periods in a year (e.g., 252 trading days)

    Returns
    -------
    float
        Annualized Sharpe ratio
    """
    equity = equity_curve["equity"]
    returns = equity.pct_change().dropna()
    if returns.std() == 0:
        return 0.0

    excess_returns = returns - risk_free_rate / periods_per_year
    sharpe_ratio = np.sqrt(periods_per_year) * excess_returns.mean() / excess_returns.std()
    return sharpe_ratio


def trade_statistics(trade_log):
    """
    Generates a summary of trades.

    Parameters
    ----------
    trade_log : list of dict

    Returns
    -------
    dict
        Statistics including total trades, wins, losses, average profit/loss, net profit
    """
    df = pd.DataFrame(trade_log)
    if df.empty:
        return {}

    trades = []
    position = {}
    for i, row in df.iterrows():
        sym = row["symbol"]
        if sym not in position:
            position[sym] = {"qty": 0, "entry_price": 0}

        if row["type"] == "BUY":
            position[sym]["qty"] += row["quantity"]
            position[sym]["entry_price"] = row["price"]
        elif row["type"] == "SELL" and position[sym]["qty"] > 0:
            profit = (row["price"] - position[sym]["entry_price"]) * position[sym]["qty"]
            trades.append(profit)
            position[sym]["qty"] = 0
            position[sym]["entry_price"] = 0

    trades = np.array(trades)
    total_trades = len(trades)
    wins = len(trades[trades > 0])
    losses = len(trades[trades <= 0])
    avg_profit = trades[trades > 0].mean() if wins > 0 else 0.0
    avg_loss = trades[trades <= 0].mean() if losses > 0 else 0.0
    net_profit = trades.sum()

    return {
        "total_trades": total_trades,
        "wins": wins,
        "losses": losses,
        "win_rate": wins / total_trades * 100 if total_trades > 0 else 0.0,
        "average_profit": avg_profit,
        "average_loss": avg_loss,
        "net_profit": net_profit
    }