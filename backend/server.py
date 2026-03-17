from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import jwt
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import threading
import time

app = Flask(__name__)
CORS(app, resources={
    r"/api/*": {
        "origins": "*",
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization", "Accept"],
        "expose_headers": ["Content-Type", "Authorization"],
        "supports_credentials": True
    }
})
# *
socketio = SocketIO(app, 
                    cors_allowed_origins="*", 
                    async_mode='gevent',  
                    ping_timeout=60,
                    ping_interval=25)

# JWT Secret Key
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'

# Simple in-memory user store
users = {}

@app.route('/api/test', methods=['GET', 'OPTIONS'])
def test_cors():
    """Test CORS configuration"""
    if request.method == 'OPTIONS':
        print("Handling OPTIONS request for /api/test")
        return jsonify({}), 200
    print("Handling GET request for /api/test")
    return jsonify({'message': 'CORS test successful', 'status': 'ok'}), 200

@app.route('/api/auth/register', methods=['POST', 'OPTIONS'])
def register():
    """Register a new user"""
    if request.method == 'OPTIONS':
        print("Handling OPTIONS request for /api/auth/register")
        return jsonify({}), 200

    try:
        data = request.get_json()

        if not data or not all(k in data for k in ['email', 'password', 'name']):
            return jsonify({'error': 'Missing required fields'}), 400

        email = data['email'].lower()
        password = data['password']
        name = data['name']

        if email in users:
            return jsonify({'error': 'User already exists'}), 409

        # Create new user
        user_id = str(len(users) + 1)
        users[email] = {
            'id': user_id,
            'email': email,
            'name': name,
            'password_hash': generate_password_hash(password),
            'created_at': datetime.datetime.utcnow().isoformat()
        }

        # Generate JWT token
        token = jwt.encode({
            'user_id': user_id,
            'email': email,
            'name': name,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7)
        }, app.config['SECRET_KEY'], algorithm='HS256')

        return jsonify({
            'token': token,
            'user': {
                'id': user_id,
                'email': email,
                'name': name
            }
        }), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/auth/login', methods=['POST', 'OPTIONS'])
def login():
    """Authenticate user and return JWT token"""
    if request.method == 'OPTIONS':
        print("Handling OPTIONS request for /api/auth/login")
        return jsonify({}), 200

    try:
        data = request.get_json()

        if not data or not all(k in data for k in ['email', 'password']):
            return jsonify({'error': 'Missing email or password'}), 400

        email = data['email'].lower()
        password = data['password']

        if email not in users:
            return jsonify({'error': 'Invalid credentials'}), 401

        user = users[email]

        # Verify password
        if not check_password_hash(user['password_hash'], password):
            return jsonify({'error': 'Invalid credentials'}), 401

        # Generate JWT token
        token = jwt.encode({
            'user_id': user['id'],
            'email': user['email'],
            'name': user['name'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7)
        }, app.config['SECRET_KEY'], algorithm='HS256')

        return jsonify({
            'token': token,
            'user': {
                'id': user['id'],
                'email': user['email'],
                'name': user['name']
            }
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/dashboard/stats', methods=['GET', 'OPTIONS'])
def get_dashboard_stats():
    """Get dashboard statistics"""
    if request.method == 'OPTIONS':
        return jsonify({}), 200

    # Mock dashboard data
    stats = {
        'totalBacktests': 24,
        'activeStrategies': 3,
        'totalPnL': 1250.75,
        'winRate': 68.5
    }

    recentBacktests = [
        {
            'id': 1,
            'strategy': 'SMA Crossover',
            'symbol': 'EURUSD',
            'pnl': 245.50,
            'date': '2024-01-15'
        },
        {
            'id': 2,
            'strategy': 'RSI Strategy',
            'symbol': 'GBPUSD',
            'pnl': -120.25,
            'date': '2024-01-14'
        },
        {
            'id': 3,
            'strategy': 'Moving Average',
            'symbol': 'USDJPY',
            'pnl': 89.30,
            'date': '2024-01-13'
        }
    ]

    return jsonify({
        'stats': stats,
        'recentBacktests': recentBacktests
    }), 200

@app.route('/api/strategies', methods=['GET', 'OPTIONS'])
def get_strategies():
    """Get available trading strategies"""
    if request.method == 'OPTIONS':
        return jsonify({}), 200

    # Mock strategies data
    strategies = [
        {
            'id': 1,
            'name': 'SMA Crossover',
            'description': 'Simple Moving Average crossover strategy',
            'parameters': {
                'fast_period': 9,
                'slow_period': 21
            },
            'active': True
        },
        {
            'id': 2,
            'name': 'RSI Strategy',
            'description': 'Relative Strength Index based strategy',
            'parameters': {
                'rsi_period': 14,
                'overbought': 70,
                'oversold': 30
            },
            'active': True
        },
        {
            'id': 3,
            'name': 'Bollinger Bands',
            'description': 'Bollinger Bands mean reversion strategy',
            'parameters': {
                'period': 20,
                'std_dev': 2
            },
            'active': False
        }
    ]

    return jsonify(strategies), 200

@app.route('/api/backtest', methods=['POST', 'OPTIONS'])
def start_backtest():
    """Start a backtest simulation"""
    if request.method == 'OPTIONS':
        return jsonify({}), 200

    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        # Validate required fields
        required_fields = ['strategy', 'symbol', 'startDate', 'endDate', 'initialCapital']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400

        # Start backtest in a separate thread to avoid blocking
        thread = threading.Thread(target=run_backtest_simulation, args=(data,))
        thread.daemon = True
        thread.start()

        return jsonify({'message': 'Backtest started successfully', 'status': 'running'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

def run_backtest_simulation(config):
    """Simulate a backtest with progress updates via Socket.IO"""
    try:
        steps = [
            "Loading data...",
            "Initializing strategy...",
            "Running simulation...",
            "Calculating metrics...",
            "Generating results..."
        ]

        for i, step in enumerate(steps):
            # Emit progress update
            socketio.emit('backtest_progress', {
                'progress': int((i + 1) / len(steps) * 100),
                'step': step
            })
            time.sleep(1)  # Simulate processing time

        # Generate mock results
        results = {
            'totalTrades': 45,
            'winningTrades': 28,
            'losingTrades': 17,
            'winRate': 62.2,
            'totalReturn': 1247.50,
            'maxDrawdown': 8.5,
            'sharpeRatio': 1.23,
            'trades': [
                {'date': '2024-01-15', 'type': 'BUY', 'price': 1.0850, 'pnl': 25.50},
                {'date': '2024-01-16', 'type': 'SELL', 'price': 1.0920, 'pnl': -15.20},
                {'date': '2024-01-17', 'type': 'BUY', 'price': 1.0880, 'pnl': 42.30},
            ]
        }

        # Emit completion
        socketio.emit('backtest_complete', {'results': results})

    except Exception as e:
        socketio.emit('backtest_error', {'error': str(e)})

if __name__ == '__main__':
    print("Starting simplified Backtester API server...")
    print("Available endpoints:")
    print("  GET  /api/test - CORS test")
    print("  POST /api/auth/register - User registration")
    print("  POST /api/auth/login - User login")
    print("\nRegistered routes:")
    for rule in app.url_map.iter_rules():
        print(f"  {rule.methods} {rule.rule}")
    print(f"\nServer will be available at http://localhost:5002")
    socketio.run(app, host='0.0.0.0', port=5002, debug=False, use_reloader=False)