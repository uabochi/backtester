from core.event import MarketEvent, SignalEvent

def test_market_event_attrs():
    e = MarketEvent({"foo": 1})
    assert e.type == "MARKET"

def test_event_queue(event_queue):
    event_queue.put("x")
    assert event_queue.get() == "x"
    assert event_queue.empty()