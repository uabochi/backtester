# Trading Strategy Backtester

A complete event-driven backtesting framework with a modern Vue.js frontend and Flask API backend.

## Project Structure

```
backtester/
├── backend/              # Python backtester (Flask API)
│   ├── core/            # Event system
│   ├── data/            # Data loading
│   ├── strategy/        # Trading strategies
│   ├── execution/       # Order execution
│   ├── portfolio/       # Position management
│   ├── performance/     # Metrics calculation
│   ├── tests/           # Unit & integration tests
│   ├── app.py           # Flask API server
│   └── requirements.txt
├── frontend/            # Vue.js frontend
│   ├── src/
│   │   ├── components/  # UI components
│   │   ├── pages/       # Page components
│   │   ├── services/    # API client
│   │   ├── stores/      # State management
│   │   └── App.vue
│   ├── package.json
│   └── vite.config.js
└── README.md
```

## Features

### Backend (Python)

- **Event-Driven Architecture**: Market events, signals, orders, fills
- **Multiple Strategies**: SMA Crossover, RSI
- **Performance Metrics**: Sharpe ratio, max drawdown, win rate
- **Data Support**: CSV files (OHLCV format)
- **REST API**: Flask-based API for frontend integration

### Frontend (Vue.js)

- **Modern UI**: Clean, responsive design
- **Interactive Charts**: Equity curves with Chart.js
- **Strategy Configuration**: Dynamic parameter forms
- **Results Visualization**: Metrics cards, trade tables
- **Real-time Updates**: Loading states and error handling

## Quick Start

### Prerequisites

- Python 3.13+
- Node.js 18+
- npm or yarn

### 1. Backend Setup

```bash
cd backend
pip install -r requirements.txt
python app.py
```

Backend API will be available at `http://localhost:5000`

### 2. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Frontend will be available at `http://localhost:5173`

### 3. Run Tests

```bash
cd backend
python -m pytest -v
```

## API Endpoints

- `POST /api/backtest` - Run a backtest
- `GET /api/strategies` - List available strategies
- `GET /api/data/files` - List available data files
- `GET /api/health` - Health check

## Deployment to Render

### Recommended: Separate Services

#### 1. Backend Web Service

- **Service Type**: Web Service
- **Runtime**: Python 3
- **Build Command**: `pip install -r backend/requirements.txt`
- **Start Command**: `cd backend && python app.py`
- **Environment Variables**:
  - `PYTHON_VERSION`: `3.13.0`

#### 2. Frontend Static Site

- **Service Type**: Static Site
- **Build Command**: `cd frontend && npm install && npm run build`
- **Publish Directory**: `frontend/dist`
- **Environment Variables**:
  - `VITE_API_URL`: `https://your-backend-service.onrender.com`

### Alternative: Single Service

For a single service deployment:

- **Service Type**: Web Service
- **Runtime**: Python 3
- **Build Command**:
  ```bash
  pip install -r backend/requirements.txt &&
  cd frontend && npm install && npm run build
  ```
- **Start Command**: `cd backend && python app.py`
- **Environment Variables**:
  - `PYTHON_VERSION`: `3.13.0`
  - `SERVE_FRONTEND`: `true`

## Environment Variables

### Backend

- `PORT`: Automatically set by Render
- `FLASK_ENV`: `production`

### Frontend

- `VITE_API_URL`: Backend service URL

### Backend Development

```bash
cd backend
# Install in development mode
pip install -e .
# Run with auto-reload
python app.py
```

### Frontend Development

```bash
cd frontend
npm run dev          # Development server
npm run build        # Production build
npm run preview      # Preview production build
```

### Testing

```bash
cd backend
pytest -v                    # Run all tests
pytest tests/test_core.py    # Run specific test file
pytest --cov                 # Run with coverage
```

## Architecture

### Event Flow

```
Data Handler → MarketEvent → Strategy → SignalEvent → Portfolio → OrderEvent → Execution → FillEvent → Portfolio Update
```

### Key Components

- **EventQueue**: Central message bus for all events
- **DataHandler**: Loads and iterates through OHLCV data
- **Strategy**: Abstract base class for trading strategies
- **Portfolio**: Manages positions, cash, and trade logging
- **ExecutionHandler**: Simulates order fills
- **Performance**: Calculates metrics and generates reports

## Configuration

### Backend

- `requirements.txt`: Python dependencies
- `app.py`: Flask configuration and routes

### Frontend

- `package.json`: Node dependencies
- `vite.config.js`: Build configuration
- `.env`: Environment variables

## Deployment

### Backend (Flask)

```bash
# Production server
gunicorn app:app -w 4 -b 0.0.0.0:5000
```

### Frontend (Vue.js)

```bash
npm run build
# Serve dist/ folder with nginx or any static server
```

### Docker (Optional)

```dockerfile
# backend/Dockerfile
FROM python:3.13
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["python", "app.py"]

# frontend/Dockerfile
FROM node:18
WORKDIR /app
COPY . .
RUN npm install && npm run build
EXPOSE 80
CMD ["npm", "run", "preview"]
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Support

For questions or issues:

- Check the documentation in `PROJECT_ARCHITECTURE.md`
- Review the API reference in `BACKEND_API_REFERENCE.md`
- Run the test suite to verify functionality
