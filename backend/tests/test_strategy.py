from strategy.sma_strategy import SMA_Crossover_Strategy
from strategy.rsi_strategy import RSI_Strategy


def test_sma_signal(handler, event_queue):
    strat = SMA_Crossover_Strategy("SYM", handler, event_queue, short_window=1, long_window=1)
    bar = handler.get_next_bar()
    strat.on_market_event(bar)
    assert not event_queue.empty()
    sig = event_queue.get()
    assert sig.type == "SIGNAL"
    assert sig.symbol == "SYM"

def test_rsi_signal(handler, event_queue):
    strat = RSI_Strategy("SYM", handler, event_queue, period=1)
    bar = handler.get_next_bar()
    strat.on_market_event(bar)
    assert not event_queue.empty()