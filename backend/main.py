"""
main.py

Integrates the entire backtesting engine:
- Loads historical data
- Initializes strategy
- Runs event-driven engine
- Updates portfolio & executes trades
- Calculates and prints performance metrics
"""

from data.data_handler import DataHandler
from core.event_queue import EventQueue
from core.event import MarketEvent
from strategy.sma_strategy import SMA_Crossover_Strategy
from execution.execution_handler import ExecutionHandler
from portfolio.portfolio import Portfolio
from performance.metrics import (
    generate_equity_curve,
    calculate_win_rate,
    calculate_max_drawdown,
    calculate_sharpe_ratio,
    trade_statistics
)


def run_backtest():
    # ----------------------
    # Initialize modules
    # ----------------------
    data_handler = DataHandler("data_files/BTCUSDT_1h.csv")
    event_queue = EventQueue()
    execution_handler = ExecutionHandler()
    portfolio = Portfolio(initial_cash=10000)
    strategy = SMA_Crossover_Strategy("BTCUSDT", data_handler, event_queue)

    # ----------------------
    # Event-driven backtest
    # ----------------------
    while data_handler.has_next():
        # Get next bar
        bar = data_handler.get_next_bar()
        market_event = MarketEvent(bar)
        event_queue.put(market_event)

        # Process all events in queue
        while not event_queue.empty():
            event = event_queue.get()

            if event.type == "MARKET":
                strategy.on_market_event(event.bar)

            elif event.type == "SIGNAL":
                order_event = portfolio.update_signal(event)
                if order_event:
                    # Execute order using current market price
                    current_price = bar["close"]
                    fill_event = execution_handler.execute_order(order_event, current_price)
                    portfolio.update_fill(fill_event)

    # ----------------------
    # Performance Metrics
    # ----------------------
    equity_curve = generate_equity_curve(portfolio.trade_log)
    win_rate = calculate_win_rate(portfolio.trade_log)
    max_dd = calculate_max_drawdown(equity_curve)
    sharpe = calculate_sharpe_ratio(equity_curve)
    stats = trade_statistics(portfolio.trade_log)

    # ----------------------
    # Print Results
    # ----------------------
    print("\n====== BACKTEST RESULTS ======")
    print(f"Final Equity: {equity_curve['equity'].iloc[-1]:.2f}")
    print(f"Win Rate: {win_rate:.2f}%")
    print(f"Max Drawdown: {max_dd:.2f}%")
    print(f"Sharpe Ratio: {sharpe:.2f}")
    print("\nTrade Summary:")
    for key, value in stats.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    run_backtest()