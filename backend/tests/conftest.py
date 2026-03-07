import sys
from pathlib import Path

# Add repo root to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from data.data_handler import DataHandler
from core.event_queue import EventQueue
from execution.execution_handler import ExecutionHandler
from portfolio.portfolio import Portfolio

@pytest.fixture
def sample_data(tmp_path):
    csv = tmp_path / "sample.csv"
    csv.write_text("timestamp,open,high,low,close,volume\n2024-01-01 00:00:00,100,101,99,100,1000\n")
    return str(csv)

@pytest.fixture
def handler(sample_data):
    return DataHandler(sample_data)

@pytest.fixture
def event_queue():
    return EventQueue()

@pytest.fixture
def exec_handler():
    return ExecutionHandler()

@pytest.fixture
def portfolio():
    return Portfolio(initial_cash=1000)