# Frontend Setup Guide

**Status:** Ready to be created  
**Stack Options:** Vue 3, React, or Svelte  
**Build Tool:** Vite (recommended) or Webpack

---

## 1. RECOMMENDED FOLDER STRUCTURE

```
project-root/
├── backend/               # Your Python backtester
│   ├── core/, data/, strategy/, ...
│   ├── main.py
│   ├── requirements.txt
│   ├── PROJECT_ARCHITECTURE.md
│   └── BACKEND_API_REFERENCE.md
│
└── frontend/              # NEW - Vue/React frontend
    ├── src/
    │   ├── components/       # Reusable components
    │   │   ├── StrategyForm.vue
    │   │   ├── ResultsChart.vue
    │   │   ├── TradesTable.vue
    │   │   └── MetricsCards.vue
    │   ├── pages/           # Page components
    │   │   ├── BacktestPage.vue
    │   │   ├── ResultsPage.vue
    │   │   └── HistoryPage.vue
    │   ├── services/        # API communication
    │   │   └── api.js       # Fetch calls to backend
    │   ├── stores/          # State management (Pinia for Vue)
    │   │   └── backtestStore.js
    │   ├── App.vue
    │   └── main.js
    ├── public/
    ├── package.json
    ├── vite.config.js
    └── .env.example
```

---

## 2. QUICK START WITH VUE 3 + VITE

### **Step 1: Create Frontend**

```bash
npm create vite@latest frontend -- --template vue
cd frontend
npm install
```

### **Step 2: Install Dependencies**

```bash
npm install axios chart.js vue-chartjs pinia
```

### **Step 3: Create Environment File**

```
# frontend/.env
VITE_API_URL=http://localhost:5000
```

### **Step 4: Create API Service**

```javascript
// frontend/src/services/api.js
import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL;

export const backtestAPI = {
  async runBacktest(params) {
    return axios.post(`${API_URL}/api/backtest`, params);
  },

  async getStrategies() {
    return axios.get(`${API_URL}/api/strategies`);
  },

  async getDataFiles() {
    return axios.get(`${API_URL}/api/data/files`);
  },

  async getBacktestResult(id) {
    return axios.get(`${API_URL}/api/backtest/${id}`);
  },
};
```

### **Step 5: Create Main Component**

```vue
<!-- frontend/src/pages/BacktestPage.vue -->
<template>
  <div class="backtest-page">
    <h1>Backtest Strategy</h1>

    <form @submit.prevent="runBacktest">
      <div>
        <label>Symbol</label>
        <select v-model="form.symbol">
          <option
            v-for="file in dataFiles"
            :key="file.name"
            :value="file.symbol"
          >
            {{ file.symbol }}
          </option>
        </select>
      </div>

      <div>
        <label>Strategy</label>
        <select v-model="form.strategy">
          <option
            v-for="strat in strategies"
            :key="strat.name"
            :value="strat.name"
          >
            {{ strat.label }}
          </option>
        </select>
      </div>

      <div v-if="strategyParams">
        <label v-for="param in strategyParams" :key="param.name">
          {{ param.name }}
          <input
            v-model="form.strategy_params[param.name]"
            :type="param.type"
            :min="param.min"
            :max="param.max"
          />
        </label>
      </div>

      <button type="submit" :disabled="loading">
        {{ loading ? "Running..." : "Run Backtest" }}
      </button>
    </form>

    <div v-if="result" class="results">
      <h2>Results</h2>
      <div class="metrics">
        <div class="metric-card">
          <h3>Total Return</h3>
          <p>{{ result.metrics.total_return }}%</p>
        </div>
        <div class="metric-card">
          <h3>Sharpe Ratio</h3>
          <p>{{ result.metrics.sharpe_ratio }}</p>
        </div>
        <div class="metric-card">
          <h3>Max Drawdown</h3>
          <p>{{ result.metrics.max_drawdown }}%</p>
        </div>
        <div class="metric-card">
          <h3>Win Rate</h3>
          <p>{{ result.metrics.win_rate }}%</p>
        </div>
      </div>

      <EquityCurveChart :data="result.equity_curve" />
      <TradesTable :trades="result.trade_log" />
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from "vue";
import { backtestAPI } from "../services/api";
import EquityCurveChart from "../components/EquityCurveChart.vue";
import TradesTable from "../components/TradesTable.vue";

const form = ref({
  symbol: "BTCUSDT",
  strategy: "sma",
  initial_cash: 10000,
  csv_file: "BTCUSDT_1h.csv",
  strategy_params: {},
});

const strategies = ref([]);
const dataFiles = ref([]);
const result = ref(null);
const loading = ref(false);

const strategyParams = computed(() => {
  return (
    strategies.value.find((s) => s.name === form.value.strategy)?.params || []
  );
});

async function loadStrategies() {
  const res = await backtestAPI.getStrategies();
  strategies.value = res.data.strategies;
}

async function loadDataFiles() {
  const res = await backtestAPI.getDataFiles();
  dataFiles.value = res.data.files;
}

async function runBacktest() {
  loading.value = true;
  try {
    const res = await backtestAPI.runBacktest(form.value);
    result.value = res.data.data;
  } catch (error) {
    alert("Error running backtest: " + error.message);
  } finally {
    loading.value = false;
  }
}

// Load data on mount
loadStrategies();
loadDataFiles();
</script>

<style scoped>
.backtest-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

form {
  background: #f5f5f5;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 30px;
}

form div {
  margin-bottom: 15px;
}

label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

input,
select {
  width: 100%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

button {
  background: #007bff;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.metrics {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 15px;
  margin-bottom: 30px;
}

.metric-card {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.metric-card h3 {
  margin: 0 0 10px 0;
  font-size: 14px;
  color: #666;
}

.metric-card p {
  margin: 0;
  font-size: 24px;
  font-weight: bold;
  color: #333;
}
</style>
```

---

## 3. SETUP BACKEND API SERVER

You'll need to wrap your Python backtester with a REST API. Choose one:

### **Option A: Flask (Lightweight)**

```bash
pip install flask flask-cors
```

```python
# backend/app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

# Import your backtester modules
from data.data_handler import DataHandler
from execution.execution_handler import ExecutionHandler
from portfolio.portfolio import Portfolio
from strategy.sma_strategy import SMA_Crossover_Strategy
from core.event_queue import EventQueue
from core.event import MarketEvent
from performance.metrics import generate_equity_curve

@app.route('/api/backtest', methods=['POST'])
def run_backtest():
    params = request.json

    handler = DataHandler(f"data_files/{params['csv_file']}")
    queue = EventQueue()
    exec_handler = ExecutionHandler()
    portfolio = Portfolio(params['initial_cash'])

    strat = SMA_Crossover_Strategy(
        params['symbol'],
        handler,
        queue,
        **params['strategy_params']
    )

    while handler.has_next():
        bar = handler.get_next_bar()
        queue.put(MarketEvent(bar))
        while not queue.empty():
            ev = queue.get()
            if ev.type == "MARKET":
                strat.on_market_event(ev.bar)
            elif ev.type == "SIGNAL":
                order = portfolio.update_signal(ev)
                if order:
                    fill = exec_handler.execute_order(order, bar["close"])
                    portfolio.update_fill(fill)

    return jsonify({
        'status': 'success',
        'data': {
            'equity_curve': generate_equity_curve(portfolio.trade_log).to_dict(),
            'trade_log': portfolio.trade_log,
            'metrics': {
                'total_trades': len(portfolio.trade_log),
                'equity_final': portfolio.equity
            }
        }
    })

@app.route('/api/strategies', methods=['GET'])
def get_strategies():
    return jsonify({
        'status': 'success',
        'strategies': [
            {
                'name': 'sma',
                'label': 'SMA Crossover',
                'params': [
                    {'name': 'short_window', 'type': 'integer', 'default': 5},
                    {'name': 'long_window', 'type': 'integer', 'default': 20}
                ]
            }
        ]
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

**Run Backend:**

```bash
python app.py
```

### **Option B: FastAPI (Modern)**

```bash
pip install fastapi uvicorn
```

```python
# backend/app.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class BacktestRequest(BaseModel):
    symbol: str
    strategy: str
    strategy_params: dict
    initial_cash: int
    csv_file: str

@app.post("/api/backtest")
async def run_backtest(request: BacktestRequest):
    # Same logic as Flask version
    pass

@app.get("/api/strategies")
async def get_strategies():
    # Return available strategies
    pass

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
```

**Run Backend:**

```bash
uvicorn app:app --reload --port 5000
```

---

## 4. RUN FRONTEND & BACKEND TOGETHER

**Terminal 1 (Backend API):**

```bash
cd backend
python app.py
# Server running at http://localhost:5000
```

**Terminal 2 (Frontend):**

```bash
cd frontend
npm run dev
# Frontend at http://localhost:5173 (Vite default)
```

Open browser to `http://localhost:5173` and enjoy!

---

## 5. DEPLOYMENT OPTIONS

### **Local Development**

- Frontend: `npm run dev` (auto-refresh on save)
- Backend: `python app.py` (Flask debug mode)

### **Production Build**

```bash
# Build frontend
cd frontend && npm run build  # Creates dist/ folder

# Serve frontend from backend
# Static files from Flask: app.static_folder = 'dist'
```

### **Docker**

```dockerfile
# Dockerfile (frontend)
FROM node:18
WORKDIR /app
COPY . .
RUN npm install && npm run build
EXPOSE 3000
CMD ["npm", "run", "preview"]
```

```dockerfile
# Dockerfile (backend)
FROM python:3.13
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["python", "app.py"]
```

---

## 6. NEXT STEPS

1. ✅ Backend complete & tested
2. ⬜ Create API server (Flask or FastAPI)
3. ⬜ Create frontend (Vue/React)
4. ⬜ Connect frontend → API endpoints
5. ⬜ Test end-to-end
6. ⬜ Deploy

Choose your framework and start with **Step 1** above!
