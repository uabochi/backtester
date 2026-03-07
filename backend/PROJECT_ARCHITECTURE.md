# Backtester Project Architecture

**Status:** Backend complete and fully tested (9/9 tests passing)  
**Last Updated:** March 6, 2026  
**Python Version:** 3.13.1

---

## 1. BACKEND STRUCTURE (Python)

```
backtester/
├── core/
│   ├── event.py              # Event classes (MarketEvent, SignalEvent, OrderEvent, FillEvent)
│   ├── event_queue.py        # EventQueue for event-driven flow
│   └── __init__.py
├── data/
│   ├── data_handler.py       # Loads & iterates through historical OHLCV data
│   ├── csv_loader.py         # CSV file loading utility
│   └── __init__.py
├── strategy/
│   ├── base_strategy.py      # Abstract Strategy class (all strategies inherit)
│   ├── sma_strategy.py       # Simple Moving Average Crossover
│   ├── rsi_strategy.py       # Relative Strength Index
│   └── __init__.py
├── execution/
│   ├── execution_handler.py  # Simulates order fills with market prices
│   └── __init__.py
├── portfolio/
│   ├── portfolio.py          # Position tracking, equity calculation, trade logging
│   ├── position.py           # Individual position management
│   ├── risk_manager.py       # Risk constraints & stop-loss logic
│   └── __init__.py
├── performance/
│   ├── metrics.py            # Equity curve generation, returns calculation
│   ├── drawdown.py           # Max drawdown & recovery analysis
│   ├── sharpe.py             # Sharpe/Sortino/Calmar ratios
│   ├── visualization.py      # Matplotlib plotting functions
│   └── __init__.py
├── utils/
│   ├── config.py             # Centralized configuration
│   ├── logger.py             # Trade logging utilities
│   └── __init__.py
├── data_files/
│   ├── BTCUSDT_1h.csv        # Sample cryptocurrency data (hourly)
│   └── EURUSD_1h.csv         # Sample forex data (hourly)
├── results/                  # Output directory (trade logs, equity curves)
├── tests/
│   ├── conftest.py           # Pytest fixtures (fixture_handler, fixture_event_queue, etc)
│   ├── test_core.py          # Event system tests
│   ├── test_data.py          # Data loading tests
│   ├── test_execution.py     # Order execution tests
│   ├── test_portfolio.py     # Portfolio management tests
│   ├── test_strategy.py      # Strategy signal generation tests
│   └── test_integration.py   # Full backtest integration test
├── main.py                   # Entry point for running backtests
└── requirements.txt          # Python dependencies
```

---

## 2. KEY BACKEND MODULES & APIs

### **core/event.py** - Event System (Foundation)

```python
# All events inherit from base Event class

MarketEvent(bar)
  └─ Signals new OHLCV data available
  └─ Fields: type="MARKET", bar={open, high, low, close, volume, timestamp}

SignalEvent(symbol, signal_type, timestamp)
  └─ Strategy generates buy/sell/hold signals
  └─ Fields: type="SIGNAL", symbol, signal_type, timestamp

OrderEvent(symbol, order_type, quantity, price, timestamp)
  └─ Portfolio converts signal to order
  └─ Fields: type="ORDER", symbol, order_type, quantity, timestamp

FillEvent(symbol, fill_type, quantity, price, timestamp)
  └─ Execution completes order
  └─ Fields: type="FILL", symbol, fill_type, quantity, price, timestamp
```

### **data/data_handler.py** - OHLCV Data Interface

```python
DataHandler(csv_file_path)
  .get_next_bar()      # Returns dict: {timestamp, open, high, low, close, volume}
  .has_next()          # Boolean check for remaining bars
  .get_latest_bars(N)  # Returns last N bars as DataFrame
```

### **strategy/base_strategy.py** - Custom Strategy Base Class

```python
Strategy(symbol, data_handler, event_queue)  # Abstract base
  .on_market_event(bar)    # Must implement: generate signals based on bar
  .generate_signal(type)   # Helper: puts SignalEvent in queue

# Implementations:
SMA_Crossover_Strategy(symbol, handler, queue, short_window=5, long_window=20)
RSI_Strategy(symbol, handler, queue, period=14, overbought=70, oversold=30)
```

### **execution/execution_handler.py** - Order Execution

```python
ExecutionHandler()
  .execute_order(order, current_price)  # Returns FillEvent with executed price
```

### **portfolio/portfolio.py** - Position & Equity Management

```python
Portfolio(initial_cash=10000)
  .update_signal(signal_event)   # Converts signal to order
  .update_fill(fill_event)       # Records trade, updates positions
  .cash                          # Current cash balance
  .equity                        # Total equity (cash + position value)
  .positions                     # Dict of open positions {symbol: {...}}
  .trade_log                     # List of all executed trades
```

### **performance/metrics.py** - Performance Calculation

```python
generate_equity_curve(trade_log)        # Returns DataFrame with equity over time
calculate_win_rate(trade_log)           # Percentage of winning trades
calculate_cagr(equity_curve)            # Compound Annual Growth Rate
calculate_sharpe_ratio(returns, rf=0.0) # Risk-adjusted returns
calculate_max_drawdown(equity_curve)    # Peak-to-trough decline
```

---

## 3. EVENT-DRIVEN FLOW (How Backtester Runs)

```
1. Data Handler loads CSV file
2. Main loop:
   ├─ Get next bar → MarketEvent → put in queue
   ├─ While queue not empty:
   │  ├─ Get event from queue
   │  ├─ IF MarketEvent:
   │  │   └─ Strategy.on_market_event(bar) → generates signals
   │  ├─ IF SignalEvent:
   │  │   ├─ Portfolio.update_signal() → creates OrderEvent
   │  │   └─ ExecutionHandler.execute_order() → creates FillEvent
   │  └─ IF FillEvent:
   │      └─ Portfolio.update_fill() → records trade, updates equity
   └─ Continue until all bars processed
3. Calculate performance metrics from trade_log
4. Output results (equity curve, trade statistics, etc.)
```

---

## 4. TESTING INFRASTRUCTURE

**Test Framework:** pytest 9.0.2  
**Coverage:** 9 tests across 6 test modules  
**Fixtures** (in conftest.py):

- `handler`: DataHandler instance
- `event_queue`: EventQueue instance
- `exec_handler`: ExecutionHandler instance
- `portfolio`: Portfolio instance
- `sample_data`: Fixture dict with sample OHLCV data

**Run Tests:**

```bash
pytest -v              # Verbose output
pytest --cov          # With coverage
pytest tests/test_core.py  # Single module
```

---

## 5. FRONTEND INTEGRATION STRATEGY

### **Option A: Separate Frontend Folder (Recommended)**

```
project-root/
├── backend/          # Your current backtester (Python)
│   ├── core/, data/, strategy/, ...
│   ├── main.py
│   ├── requirements.txt
│   └── (REST API server - Flask/FastAPI)
│
└── frontend/         # Vue/React/etc (JavaScript/TypeScript)
    ├── src/
    ├── public/
    ├── package.json
    └── API calls to http://localhost:5000 (backend)
```

**Pros:**

- Clear separation of concerns
- Frontend & backend can be deployed independently
- Easier to scale frontend separately
- Standard industry practice

### **Option B: Monorepo (All in one folder)**

```
backtester/
├── backend/
│   ├── core/, data/, strategy/, ...
│   └── api/          # New Flask/FastAPI server
├── frontend/
│   ├── src/, public/, ...
│   └── package.json
└── docker-compose.yml
```

**Pros:**

- Single repository to clone
- Easier local development
- Deployment can be orchestrated

---

## 6. BACKEND API LAYER (To Be Created)

Since Python backtester is not a web service, you'll need a lightweight REST API wrapper:

### **Recommended Stack:** Flask or FastAPI

```python
# Example API endpoints the frontend will call:

POST /api/backtest
  Input: {
    "symbol": "BTCUSDT",
    "strategy": "sma",
    "strategy_params": {"short_window": 5, "long_window": 20},
    "initial_cash": 10000,
    "csv_file": "BTCUSDT_1h.csv"
  }
  Output: {
    "status": "success",
    "equity_curve": [...],
    "trade_log": [...],
    "metrics": {
      "total_return": 15.5,
      "sharpe_ratio": 1.23,
      "max_drawdown": -8.2,
      "win_rate": 62.5
    }
  }

GET /api/data/symbols
  Output: ["BTCUSDT", "EURUSD"]

GET /api/strategies
  Output: ["sma", "rsi", "custom"]

GET /api/results/:backtest_id
  Output: {equity_curve, trades, metrics}
```

---

## 7. IMPORTANT CONVENTIONS & GOTCHAS

### **Data Format**

- All OHLCV data as dictionaries with keys: `timestamp`, `open`, `high`, `low`, `close`, `volume`
- Timestamps should be sortable (ISO format or numeric)
- CSVs must have header row with these column names

### **Event Flow**

- **DO NOT** put dict in queue; use Event objects (MarketEvent, SignalEvent, etc.)
- Strategy.generate_signal() must be called with signal_type: "BUY", "SELL", or "HOLD"
- All events have a `.type` attribute: "MARKET", "SIGNAL", "ORDER", "FILL"

### **Portfolio Updates**

- Signals must go through `portfolio.update_signal()` (converts to OrderEvent)
- Fills must go through `portfolio.update_fill()` (records trade)
- `portfolio.trade_log` accumulates all trades (used for metrics)

### **Testing**

- conftest.py provides fixtures; don't create duplicate instances
- Use `from core.event import SignalEvent` not dict comprehension
- Integration test checks strategy runs without errors, not profitability

---

## 8. CONFIGURATION MANAGEMENT

**Current:** utils/config.py (centralized settings)  
**Future:** Will expand to:

- API server settings (host, port, debug mode)
- Database connection strings (if adding persistence)
- CORS settings for frontend
- Strategy parameters defaults

---

## 9. DEPLOYMENT CHECKLIST (When Ready)

- [ ] Create Flask/FastAPI wrapper for backtester
- [ ] Add database layer (optional: store backtests)
- [ ] Create frontend (Vue/React)
- [ ] Set up CORS for API
- [ ] Docker containers for both backend & frontend
- [ ] nginx reverse proxy (if needed)
- [ ] Cloud deployment (AWS/GCP/Heroku)

---

## 10. QUICK REFERENCE: HOW TO RUN

**Backend (Python):**

```bash
python main.py
```

**Backtests (Tests):**

```bash
pytest -v
```

**Frontend (After Setup):**

```bash
cd frontend && npm start
```

**Full Stack (Docker, if set up):**

```bash
docker-compose up
```

---

## Contact Points for Confusion

If frontend development gets confusing, refer to:

1. **data/data_handler.py** - How CSV is loaded
2. **strategy/base_strategy.py** - How signals are generated
3. **performance/metrics.py** - What metrics the frontend can display
4. **tests/test_integration.py** - Real-world example of backtest flow
