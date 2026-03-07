"""
visualization.py

Plots backtesting results:
- Equity curve
- Trades on price chart (BUY/SELL markers)
"""

import matplotlib.pyplot as plt
import pandas as pd


def plot_equity_curve(equity_curve):
    """
    Plots the equity curve.

    Parameters
    ----------
    equity_curve : pd.DataFrame
        Must contain 'timestamp' and 'equity' columns
    """
    plt.figure(figsize=(12, 6))
    plt.plot(equity_curve['timestamp'], equity_curve['equity'], label='Equity Curve', color='blue')
    plt.title('Equity Curve')
    plt.xlabel('Time')
    plt.ylabel('Equity')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def plot_trades(price_data, trade_log, symbol="BTCUSDT"):
    """
    Plots trades on the price chart with BUY/SELL markers.

    Parameters
    ----------
    price_data : pd.DataFrame
        Must contain 'timestamp', 'open', 'high', 'low', 'close'
    trade_log : list of dict
        Must contain 'symbol', 'type' ('BUY'/'SELL'), 'price', 'timestamp'
    symbol : str
        Trading symbol to filter trades
    """
    price_data = price_data.copy()
    price_data = price_data.sort_values("timestamp").reset_index(drop=True)

    plt.figure(figsize=(14, 6))
    plt.plot(price_data['timestamp'], price_data['close'], label='Close Price', color='black')

    # Extract trades for this symbol
    trades_df = pd.DataFrame(trade_log)
    trades_df = trades_df[trades_df['symbol'] == symbol]

    if not trades_df.empty:
        # Plot BUY trades
        buy_trades = trades_df[trades_df['type'] == 'BUY']
        plt.scatter(buy_trades['timestamp'], buy_trades['price'],
                    marker='^', color='green', label='BUY', s=100)

        # Plot SELL trades
        sell_trades = trades_df[trades_df['type'] == 'SELL']
        plt.scatter(sell_trades['timestamp'], sell_trades['price'],
                    marker='v', color='red', label='SELL', s=100)

    plt.title(f'{symbol} Price Chart with Trades')
    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def plot_backtest_results(price_data, trade_log, equity_curve, symbol="BTCUSDT"):
    """
    Combined plotting: equity curve + price chart with trades.

    Parameters
    ----------
    price_data : pd.DataFrame
        Historical OHLCV data
    trade_log : list of dict
        Trade history
    equity_curve : pd.DataFrame
        Equity curve from portfolio
    symbol : str
        Trading symbol
    """
    plot_equity_curve(equity_curve)
    plot_trades(price_data, trade_log, symbol=symbol)