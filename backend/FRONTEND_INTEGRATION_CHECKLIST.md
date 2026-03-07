# Frontend Integration Checklist

**Objective:** Integrate frontend with the Python backtester backend  
**Current Status:** Backend ready (all tests passing, API layer needed)  
**Timeline:** 3-5 days for complete frontend + integration

---

## PHASE 1: API SERVER (1 day)

- [ ] Choose framework: **Flask** (lightweight) or **FastAPI** (modern)
- [ ] Install dependencies: `pip install flask flask-cors` or `pip install fastapi uvicorn`
- [ ] Create `backend/app.py` with endpoints:
  - [ ] `POST /api/backtest` → runs backtest
  - [ ] `GET /api/strategies` → returns available strategies
  - [ ] `GET /api/data/files` → returns available CSV files
  - [ ] `GET /api/backtest/:id` → returns saved result
  - [ ] `GET /api/backtests` → lists all results
- [ ] Add CORS middleware for frontend communication
- [ ] **Test:** `curl -X POST http://localhost:5000/api/backtest -H "Content-Type: application/json" -d '{...}'`
- [ ] Verify response format matches BACKEND_API_REFERENCE.md

---

## PHASE 2: FRONTEND STRUCTURE (1 day)

- [ ] Create frontend folder: `npm create vite@latest frontend -- --template vue`
- [ ] Install dependencies: `npm install axios chart.js vue-chartjs pinia`
- [ ] Create folder structure:
  - [ ] `src/components/` (StrategyForm, ResultsChart, TradesTable, MetricsCards)
  - [ ] `src/pages/` (BacktestPage, ResultsPage)
  - [ ] `src/services/` (api.js with axios calls)
  - [ ] `src/stores/` (Pinia store for state management)
- [ ] Create `.env` file with `VITE_API_URL=http://localhost:5000`

---

## PHASE 3: CORE COMPONENTS (1 day)

### Strategy Form Component

- [ ] Dropdown to select symbol (BTCUSDT, EURUSD, etc.)
- [ ] Dropdown to select strategy (SMA, RSI, etc.)
- [ ] Dynamic parameter inputs (short_window, long_window, period, overbought, oversold)
- [ ] Initial cash input (input type="number")
- [ ] Submit button that calls `backtestAPI.runBacktest()`
- [ ] Loading state during backtest run
- [ ] Error handling with user-friendly messages

### Results Display

- [ ] Metrics cards (Total Return, Sharpe Ratio, Max Drawdown, Win Rate)
- [ ] Equity curve chart (LineChart with Chart.js)
- [ ] Trades table (symbol, type, quantity, price, timestamp, cash, equity)
- [ ] Export buttons (CSV download for trades & equity curve)

---

## PHASE 4: API INTEGRATION (1 day)

### API Service Setup

- [ ] Create `frontend/src/services/api.js`
- [ ] Export functions: `runBacktest()`, `getStrategies()`, `getDataFiles()`, etc.
- [ ] Handle errors: `try/catch` with user-friendly messages
- [ ] Handle loading states

### State Management (Pinia)

- [ ] Create store: `useBacktestStore()`
- [ ] State: `backtest`, `loading`, `error`, `results`
- [ ] Actions: `runBacktest()`, `getStrategies()`, `getDataFiles()`
- [ ] Getters: `isLoading`, `hasResults`, `getMetrics`

### Page Components

- [ ] `BacktestPage.vue`: Form + submit → calls store actions
- [ ] `ResultsPage.vue`: Displays equity curve, trades, metrics
- [ ] `HistoryPage.vue`: List of past backtests (if persisting to database)

---

## PHASE 5: STYLING & UX (0.5-1 day)

- [ ] Choose CSS framework (Tailwind, Bootstrap, or plain CSS)
- [ ] Create responsive layout:
  - [ ] Mobile-friendly form
  - [ ] Side-by-side form + chart on desktop
  - [ ] Full-width trades table
- [ ] Add loading spinners during backtest
- [ ] Add success/error toast notifications
- [ ] Nice color scheme for metrics
- [ ] Chart animations

---

## PHASE 6: TESTING & DEBUGGING (1 day)

- [ ] **Backend testing:**
  - [ ] Run `python app.py` in one terminal
  - [ ] Test all API endpoints with curl or Postman
  - [ ] Verify response formats match spec

- [ ] **Frontend testing:**
  - [ ] Run `npm run dev` in another terminal
  - [ ] Open http://localhost:5173
  - [ ] Submit a backtest
  - [ ] Verify chart displays
  - [ ] Verify trades table populates
  - [ ] Verify metrics cards show correct values

- [ ] **E2E testing:**
  - [ ] Form → API → Results display → Export
  - [ ] Error handling (bad CSV, invalid params, etc.)
  - [ ] Edge cases (no trades, single trade, negative return)

---

## PHASE 7: ENHANCEMENTS (Optional)

- [ ] Database persistence (save/load backtests)
- [ ] User authentication
- [ ] Strategy comparison (run multiple strategies side-by-side)
- [ ] Parameter optimization (test ranges of parameters)
- [ ] Real-time progress streaming (WebSocket)
- [ ] Download results as PDF report
- [ ] Dark mode theme

---

## QUICK START COMMANDS

### Terminal 1: Backend API

```bash
cd backend
pip install flask flask-cors  # Or: pip install fastapi uvicorn
python app.py
# Server at http://localhost:5000
```

### Terminal 2: Frontend Dev

```bash
cd frontend
npm install
npm run dev
# Frontend at http://localhost:5173
```

### Terminal 3: Debug

```bash
# Test API endpoint
curl -X POST http://localhost:5000/api/backtest \
  -H "Content-Type: application/json" \
  -d '{"symbol":"BTCUSDT","strategy":"sma","strategy_params":{"short_window":5,"long_window":20},"initial_cash":10000,"csv_file":"BTCUSDT_1h.csv"}'

# Mockoon for API testing (download free GUI tool)
# Or use Postman
```

---

## FILE REFERENCES

**When you get confused, read these in order:**

1. `PROJECT_ARCHITECTURE.md` → Big picture (read first!)
2. `BACKEND_API_REFERENCE.md` → Exact API specs
3. `FRONTEND_SETUP.md` → Step-by-step frontend setup
4. Test files → See real usage examples:
   - `tests/test_integration.py` → Full backtest flow
   - `tests/test_strategy.py` → Strategy usage
   - `tests/test_portfolio.py` → Portfolio updates

---

## KEY DECISION POINTS

**Which CSS framework?**

- Tailwind: Modern, utility-first, great with Vue
- Bootstrap: Classic, quick setup, lots of examples
- Plain CSS: Full control, more code

**Flask vs FastAPI?**

- Flask: Simpler, good for small projects, more tutorials
- FastAPI: Faster, better type hints, automatic docs
  → **Recommend Flask for simplicity**

**Where to save backtests?**

- Option A: SQLite (lightweight, no server)
- Option B: PostgreSQL (scalable, better performance)
- Option C: File system (simple but slow)
  → **Start with SQLite, upgrade if needed**

**How to handle real-time progress?**

- Option A: Return results after backtest completes (current plan)
- Option B: WebSocket for streaming updates
  → **Start with A, add B if needed**

---

## TROUBLESHOOTING

**Symptom:** CORS errors in browser console  
**Fix:** Add `flask_cors.CORS(app)` to backend OR use proxy in vite.config.js

**Symptom:** API returns 404 for `/api/backtest`  
**Fix:** Check Flask route is `@app.route('/api/backtest', methods=['POST'])`

**Symptom:** Frontend makes API call but nothing happens  
**Fix:** Check Network tab in browser DevTools, verify URL & method match

**Symptom:** Chart doesn't display  
**Fix:** Check data format (should be array of {timestamp, equity} objects)

**Symptom:** Trade log shows but chart is empty  
**Fix:** Check if `generate_equity_curve()` is being called with correct trade_log

---

## SUCCESS CRITERIA

✅ Backend API server runs  
✅ Frontend loads without errors  
✅ Form allows strategy selection + parameters  
✅ Clicking "Run Backtest" hits `/api/backtest` endpoint  
✅ Results return and display in 5-30 seconds  
✅ Equity curve chart renders  
✅ Trades table shows all executed trades  
✅ Metrics cards show correct values (return, Sharpe, drawdown, win rate)  
✅ Export to CSV works  
✅ Error messages display for invalid inputs

When all ✅, frontend integration is **COMPLETE**!
