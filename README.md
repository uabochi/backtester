# Traders Casa - Professional Trading Backtester

A comprehensive trading strategy backtesting platform built with Vue.js 3 and Python Flask, featuring TradingView-like charts and real-time backtesting capabilities.

## Features

### Frontend (Vue.js 3)

- **Modern SPA Architecture**: Built with Vue 3 Composition API, Vue Router, and Pinia state management
- **TradingView-like Charts**: Professional charting with Lightweight Charts library
- **Real-time Backtesting**: Live progress updates via Socket.io
- **Multi-user Authentication**: JWT-based authentication system
- **Professional UI**: Tailwind CSS with custom trading-focused design
- **Interactive Strategy Builder**: Create and manage trading strategies with custom parameters

### Backend (Python Flask)

- **RESTful API**: Complete API for user management, strategies, and backtesting
- **Real-time Communication**: Socket.io integration for live backtest progress
- **Database Integration**: Ready for PostgreSQL/SQLite with SQLAlchemy
- **Strategy Engine**: Modular strategy system with parameter optimization

## Project Structure

```
backtester/
├── frontend/                 # Vue.js SPA
│   ├── src/
│   │   ├── components/       # Reusable Vue components
│   │   │   ├── layout/       # Layout components (Header, etc.)
│   │   │   └── ui/           # UI components (Buttons, Modals, etc.)
│   │   ├── views/            # Page components
│   │   │   ├── Dashboard.vue # Main dashboard
│   │   │   ├── Backtest.vue  # Backtesting interface
│   │   │   ├── Strategies.vue # Strategy management
│   │   │   ├── History.vue   # Backtest history
│   │   │   ├── Login.vue     # Authentication
│   │   │   ├── Register.vue  # User registration
│   │   │   └── Profile.vue   # User profile management
│   │   ├── stores/           # Pinia stores
│   │   │   ├── auth.js       # Authentication state
│   │   │   └── backtest.js   # Backtest state management
│   │   ├── router.js         # Vue Router configuration
│   │   └── main.js           # App entry point
│   ├── package.json          # Frontend dependencies
│   └── vite.config.js        # Vite configuration
├── core/                     # Python backend core
│   ├── engine.py             # Backtesting engine
│   ├── event_queue.py        # Event system
│   ├── event.py              # Event definitions
│   └── ...
├── strategies/               # Trading strategies
│   ├── base_strategy.py      # Base strategy class
│   ├── sma_crossover.py      # Example strategy
│   └── ...
├── data/                     # Data management
├── portfolio/                # Portfolio management
├── visualization/            # Chart generation
└── main.py                   # Flask application entry point
```

## Quick Start

### Prerequisites

- Node.js 16+ and npm
- Python 3.8+
- Git

### Frontend Setup

1. **Navigate to frontend directory:**

   ```bash
   cd frontend
   ```

2. **Install dependencies:**

   ```bash
   npm install
   ```

3. **Start development server:**

   ```bash
   npm run dev
   ```

4. **Build for production:**
   ```bash
   npm run build
   ```

### Backend Setup

1. **Install Python dependencies:**

   ```bash
   pip install flask flask-socketio flask-cors python-socketio
   ```

2. **Run the Flask server:**
   ```bash
   python main.py
   ```

## Key Components

### TradingChart.vue

Professional chart component with:

- Multiple timeframe support
- Drawing tools (trend lines, rectangles, etc.)
- Trade markers and annotations
- Real-time data updates

### Backtest.vue

Comprehensive backtesting interface featuring:

- Strategy parameter adjustment
- Real-time progress tracking
- Interactive charts
- Performance metrics display

### Strategies.vue

Strategy management system with:

- Create/edit/delete strategies
- Parameter configuration
- Strategy performance tracking

### History.vue

Backtest history and analytics with:

- Filterable results
- Detailed performance metrics
- Re-run capabilities

## API Endpoints

### Authentication

- `POST /api/auth/login` - User login
- `POST /api/auth/register` - User registration
- `POST /api/auth/logout` - User logout

### Strategies

- `GET /api/strategies` - List user strategies
- `POST /api/strategies` - Create new strategy
- `PUT /api/strategies/:id` - Update strategy
- `DELETE /api/strategies/:id` - Delete strategy

### Backtests

- `GET /api/backtests` - List backtest history
- `POST /api/backtests` - Start new backtest
- `GET /api/backtests/:id` - Get backtest details
- `DELETE /api/backtests/:id` - Delete backtest

### User Management

- `GET /api/user/profile` - Get user profile
- `PUT /api/user/profile` - Update profile
- `POST /api/user/change-password` - Change password

## Deployment

### Render Deployment

1. Connect your GitHub repository to Render
2. Set up two services:
   - **Web Service**: For the Flask backend
   - **Static Site**: For the Vue.js frontend
3. Configure environment variables
4. Deploy and enjoy!

### Environment Variables

```env
FLASK_ENV=production
SECRET_KEY=your-secret-key
DATABASE_URL=your-database-url
JWT_SECRET_KEY=your-jwt-secret
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For questions or support, please open an issue on GitHub or contact the development team.

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
