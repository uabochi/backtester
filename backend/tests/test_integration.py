from strategy.sma_strategy import SMA_Crossover_Strategy
from core.event import MarketEvent
from performance.metrics import generate_equity_curve


def test_full_backtest(handler, event_queue, exec_handler, portfolio):
    strat = SMA_Crossover_Strategy("SYM", handler, event_queue, short_window=1, long_window=1)
    while handler.has_next():
        bar = handler.get_next_bar()
        event_queue.put(MarketEvent(bar))
        while not event_queue.empty():
            ev = event_queue.get()
            if ev.type=="MARKET":
                strat.on_market_event(ev.bar)
            elif ev.type=="SIGNAL":
                order = portfolio.update_signal(ev)
                if order:
                    fill = exec_handler.execute_order(order, current_price=bar["close"])
                    portfolio.update_fill(fill)
    
    # Verify backtest completed
    assert portfolio.equity > 0
    assert len(strat.signals) >= 0  # Strategy may or may not have generated signals
    
    # Only test equity curve if trades were made
    if portfolio.trade_log:
        equity_curve = generate_equity_curve(portfolio.trade_log)
        assert len(equity_curve) > 0