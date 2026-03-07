import pytest
from data.data_handler import DataHandler


def test_load_and_iterate(handler):
    assert handler.has_next()
    bar = handler.get_next_bar()
    assert bar["open"] == 100
    assert not handler.data.empty

def test_validation_error(tmp_path):
    bad = tmp_path / "bad.csv"
    bad.write_text("foo,bar\n1,2\n")
    with pytest.raises(ValueError):
        DataHandler(str(bad))