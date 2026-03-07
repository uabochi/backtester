# Backend API Reference

**Purpose:** Specification for REST API that frontend will call  
**Framework Recommendation:** Flask or FastAPI (Python)  
**Base URL:** `http://localhost:5000` (development)

---

## 1. RUN BACKTEST

**Endpoint:** `POST /api/backtest`

**Request Body:**

```json
{
  "symbol": "BTCUSDT",
  "strategy": "sma",
  "strategy_params": {
    "short_window": 5,
    "long_window": 20
  },
  "initial_cash": 10000,
  "csv_file": "BTCUSDT_1h.csv"
}
```

**Response (Success 200):**

```json
{
  "status": "success",
  "backtest_id": "bf47e8c2-1a3b-4c5d-8e91-2f3c4d5e6f7a",
  "data": {
    "equity_curve": [
      {"timestamp": "2024-01-01", "equity": 10000},
      {"timestamp": "2024-01-02", "equity": 10150},
      ...
    ],
    "trade_log": [
      {
        "symbol": "BTCUSDT",
        "type": "BUY",
        "quantity": 1,
        "price": 45000,
        "timestamp": "2024-01-01",
        "cash": 9550,
        "equity": 10000
      },
      ...
    ],
    "metrics": {
      "total_return": 15.5,
      "sharpe_ratio": 1.23,
      "max_drawdown": -8.2,
      "win_rate": 62.5,
      "total_trades": 8,
      "winning_trades": 5
    }
  }
}
```

**Response (Error 400):**

```json
{
  "status": "error",
  "message": "CSV file not found or invalid strategy"
}
```

---

## 2. GET AVAILABLE DATA FILES

**Endpoint:** `GET /api/data/files`

**Response:**

```json
{
  "status": "success",
  "files": [
    {
      "name": "BTCUSDT_1h.csv",
      "symbol": "BTCUSDT",
      "rows": 730,
      "date_range": "2023-01-01 to 2023-12-31"
    },
    {
      "name": "EURUSD_1h.csv",
      "symbol": "EURUSD",
      "rows": 730,
      "date_range": "2023-01-01 to 2023-12-31"
    }
  ]
}
```

---

## 3. GET AVAILABLE STRATEGIES

**Endpoint:** `GET /api/strategies`

**Response:**

```json
{
  "status": "success",
  "strategies": [
    {
      "name": "sma",
      "label": "SMA Crossover",
      "description": "Simple Moving Average crossover strategy",
      "params": [
        {
          "name": "short_window",
          "type": "integer",
          "default": 5,
          "min": 1,
          "max": 50,
          "description": "Short-term MA window"
        },
        {
          "name": "long_window",
          "type": "integer",
          "default": 20,
          "min": 1,
          "max": 200,
          "description": "Long-term MA window"
        }
      ]
    },
    {
      "name": "rsi",
      "label": "RSI Strategy",
      "description": "Relative Strength Index strategy",
      "params": [
        {
          "name": "period",
          "type": "integer",
          "default": 14,
          "min": 2,
          "max": 50
        },
        {
          "name": "overbought",
          "type": "integer",
          "default": 70,
          "min": 50,
          "max": 100
        },
        {
          "name": "oversold",
          "type": "integer",
          "default": 30,
          "min": 0,
          "max": 50
        }
      ]
    }
  ]
}
```

---

## 4. GET BACKTEST RESULT BY ID

**Endpoint:** `GET /api/backtest/:id`

**Response:**

```json
{
  "status": "success",
  "backtest_id": "bf47e8c2-1a3b-4c5d-8e91-2f3c4d5e6f7a",
  "created_at": "2024-01-15T10:30:00Z",
  "params": {
    "symbol": "BTCUSDT",
    "strategy": "sma",
    "strategy_params": {...}
  },
  "data": {
    "equity_curve": [...],
    "trade_log": [...],
    "metrics": {...}
  }
}
```

---

## 5. LIST ALL BACKTESTS

**Endpoint:** `GET /api/backtests`

**Query Parameters:**

- `limit`: Number of results (default: 20)
- `offset`: Pagination offset (default: 0)
- `symbol`: Filter by symbol (optional)

**Response:**

```json
{
  "status": "success",
  "total": 45,
  "limit": 20,
  "offset": 0,
  "backtests": [
    {
      "id": "bf47e8c2-1a3b-4c5d-8e91-2f3c4d5e6f7a",
      "symbol": "BTCUSDT",
      "strategy": "sma",
      "created_at": "2024-01-15T10:30:00Z",
      "metrics": {
        "total_return": 15.5,
        "sharpe_ratio": 1.23,
        "max_drawdown": -8.2
      }
    },
    ...
  ]
}
```

---

## 6. DELETE BACKTEST RESULT

**Endpoint:** `DELETE /api/backtest/:id`

**Response:**

```json
{
  "status": "success",
  "message": "Backtest deleted"
}
```

---

## 7. EXPORT TRADE LOG

**Endpoint:** `GET /api/backtest/:id/trades.csv`

**Response:** CSV file download

```
symbol,type,quantity,price,timestamp,cash,equity
BTCUSDT,BUY,1,45000,2024-01-01,9550,10000
BTCUSDT,SELL,1,46000,2024-01-02,10550,10550
```

---

## 8. EXPORT EQUITY CURVE

**Endpoint:** `GET /api/backtest/:id/equity.csv`

**Response:** CSV file download

```
timestamp,equity
2024-01-01,10000
2024-01-02,10150
2024-01-03,10300
```

---

## ERROR CODES

| Code | Meaning                      |
| ---- | ---------------------------- |
| 200  | Success                      |
| 400  | Bad request (invalid params) |
| 404  | Resource not found           |
| 422  | Validation error             |
| 500  | Server error                 |

**Error Response Format:**

```json
{
  "status": "error",
  "code": 400,
  "message": "Invalid strategy_params",
  "details": {
    "short_window": "must be integer between 1 and 50"
  }
}
```

---

## IMPLEMENTATION NOTES

### Within Backend Layer (Python)

```python
# The API will call these existing backend functions:

from data.data_handler import DataHandler
from execution.execution_handler import ExecutionHandler
from portfolio.portfolio import Portfolio
from strategy.sma_strategy import SMA_Crossover_Strategy
from performance.metrics import generate_equity_curve, calculate_sharpe_ratio

def run_backtest(symbol, strategy, params, initial_cash, csv_file):
    handler = DataHandler(csv_file)
    event_queue = EventQueue()
    exec_handler = ExecutionHandler()
    portfolio = Portfolio(initial_cash)

    strat = SMA_Crossover_Strategy(symbol, handler, event_queue, **params)

    # Event loop...
    while handler.has_next():
        # ... process events

    return {
      'equity_curve': generate_equity_curve(portfolio.trade_log),
      'trade_log': portfolio.trade_log,
      'metrics': calculate_metrics(portfolio.trade_log)
    }
```

### Frontend Consumption (JavaScript/Vue)

```javascript
// Frontend will call endpoints like:

async function runBacktest(params) {
  const response = await fetch("/api/backtest", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(params),
  });

  const result = await response.json();

  // Display equity_curve as chart
  // Display trade_log as table
  // Display metrics as cards
}
```

---

## FUTURE ENHANCEMENTS

- [ ] Batch backtests (run multiple strategies simultaneously)
- [ ] Optimization endpoint (test parameter ranges)
- [ ] Real-time backtest progress streaming (WebSocket)
- [ ] Database persistence (save/load backtests)
- [ ] User authentication & saved portfolios
- [ ] Parameter sensitivity analysis
