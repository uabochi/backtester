def test_fill(exec_handler):
    class Dummy: symbol="SYM"; order_type="BUY"; quantity=1; price=5
    fill = exec_handler.execute_order(Dummy(), current_price=6)
    assert fill.price == 6