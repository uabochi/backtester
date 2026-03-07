def test_portfolio_trade(portfolio):
    # simulate signal event
    from core.event import SignalEvent
    sig = SignalEvent("SYM", "BUY", "2024-01-01")
    order = portfolio.update_signal(sig)
    assert order.symbol == "SYM"
    fill = type("F",(object,),{"symbol":"SYM","quantity":1,"price":10,"fill_type":"BUY","timestamp":"2024-01-01"})()
    portfolio.update_fill(fill)
    assert portfolio.cash < portfolio.equity