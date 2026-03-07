"""
Flask API server for the backtester backend.
Provides REST endpoints for frontend integration.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import os
import time

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication
socketio = SocketIO(app, cors_allowed_origins="*")

# Store active backtest sessions
backtest_sessions = {}

# Import backtester modules
from core.event import MarketEvent
from core.event_queue import EventQueue
from data.data_handler import DataHandler
from execution.execution_handler import ExecutionHandler
from portfolio.portfolio import Portfolio
from strategy.sma_strategy import SMA_Crossover_Strategy
from strategy.rsi_strategy import RSI_Strategy
from performance.metrics import generate_equity_curve

@app.route('/api/backtest', methods=['POST'])
def run_backtest():
    """
    Run a backtest with the given parameters.
    """
    try:
        params = request.json

        # Validate required parameters
        required = ['symbol', 'strategy', 'strategy_params', 'initial_cash', 'csv_file']
        for req in required:
            if req not in params:
                return jsonify({
                    'status': 'error',
                    'message': f'Missing required parameter: {req}'
                }), 400

        # Initialize components
        csv_path = os.path.join(os.path.dirname(__file__), 'data_files', params['csv_file'])
        if not os.path.exists(csv_path):
            return jsonify({
                'status': 'error',
                'message': f'CSV file not found: {params["csv_file"]}'
            }), 404

        handler = DataHandler(csv_path)
        event_queue = EventQueue()
        exec_handler = ExecutionHandler()
        portfolio = Portfolio(params['initial_cash'])

        # Create strategy
        strategy_name = params['strategy']
        if strategy_name == 'sma':
            strategy = SMA_Crossover_Strategy(
                params['symbol'],
                handler,
                event_queue,
                **params['strategy_params']
            )
        elif strategy_name == 'rsi':
            strategy = RSI_Strategy(
                params['symbol'],
                handler,
                event_queue,
                **params['strategy_params']
            )
        else:
            return jsonify({
                'status': 'error',
                'message': f'Unknown strategy: {strategy_name}'
            }), 400

        # Run backtest
        while handler.has_next():
            bar = handler.get_next_bar()
            event_queue.put(MarketEvent(bar))

            while not event_queue.empty():
                ev = event_queue.get()
                if ev.type == "MARKET":
                    strategy.on_market_event(ev.bar)
                elif ev.type == "SIGNAL":
                    order = portfolio.update_signal(ev)
                    if order:
                        fill = exec_handler.execute_order(order, bar["close"])
                        portfolio.update_fill(fill)

        # Generate results
        equity_curve = generate_equity_curve(portfolio.trade_log)

        # Calculate basic metrics
        total_trades = len(portfolio.trade_log)
        winning_trades = len([t for t in portfolio.trade_log if t.get('type') == 'SELL' and t.get('price', 0) > 0])
        win_rate = (winning_trades / total_trades * 100) if total_trades > 0 else 0

        # Calculate returns
        initial_equity = params['initial_cash']
        final_equity = portfolio.equity
        total_return = ((final_equity - initial_equity) / initial_equity * 100) if initial_equity > 0 else 0

        return jsonify({
            'status': 'success',
            'backtest_id': f"bt_{hash(str(params)) % 1000000}",
            'data': {
                'equity_curve': equity_curve.to_dict('records') if not equity_curve.empty else [],
                'trade_log': portfolio.trade_log,
                'metrics': {
                    'total_return': round(total_return, 2),
                    'final_equity': round(final_equity, 2),
                    'total_trades': total_trades,
                    'winning_trades': winning_trades,
                    'win_rate': round(win_rate, 2),
                    'sharpe_ratio': 0.0,  # Placeholder - would need more complex calculation
                    'max_drawdown': 0.0   # Placeholder - would need calculation
                }
            }
        })

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Backtest failed: {str(e)}'
        }), 500

@app.route('/api/strategies', methods=['GET'])
def get_strategies():
    """
    Return available strategies and their parameters.
    """
    return jsonify({
        'status': 'success',
        'strategies': [
            {
                'name': 'sma',
                'label': 'SMA Crossover',
                'description': 'Simple Moving Average crossover strategy',
                'params': [
                    {
                        'name': 'short_window',
                        'type': 'integer',
                        'default': 5,
                        'min': 1,
                        'max': 50,
                        'description': 'Short-term MA window'
                    },
                    {
                        'name': 'long_window',
                        'type': 'integer',
                        'default': 20,
                        'min': 1,
                        'max': 200,
                        'description': 'Long-term MA window'
                    }
                ]
            },
            {
                'name': 'rsi',
                'label': 'RSI Strategy',
                'description': 'Relative Strength Index strategy',
                'params': [
                    {
                        'name': 'period',
                        'type': 'integer',
                        'default': 14,
                        'min': 2,
                        'max': 50,
                        'description': 'RSI calculation period'
                    },
                    {
                        'name': 'overbought',
                        'type': 'integer',
                        'default': 70,
                        'min': 50,
                        'max': 100,
                        'description': 'Overbought threshold'
                    },
                    {
                        'name': 'oversold',
                        'type': 'integer',
                        'default': 30,
                        'min': 0,
                        'max': 50,
                        'description': 'Oversold threshold'
                    }
                ]
            }
        ]
    })

@app.route('/api/data/options', methods=['GET'])
def get_data_options():
    """
    Return available symbols and timeframes for data selection.
    """
    try:
        data_files_dir = os.path.join(os.path.dirname(__file__), 'data_files')
        if not os.path.exists(data_files_dir):
            return jsonify({
                'status': 'error',
                'message': 'Data files directory not found'
            }), 404

        symbols = set()
        timeframes = set()
        data_files = {}

        for filename in os.listdir(data_files_dir):
            if filename.endswith('.csv'):
                # Parse filename like BTCUSDT_1h.csv
                parts = filename.replace('.csv', '').split('_')
                if len(parts) == 2:
                    symbol, timeframe = parts
                    symbols.add(symbol)
                    timeframes.add(timeframe)

                    filepath = os.path.join(data_files_dir, filename)
                    file_size = os.path.getsize(filepath)
                    with open(filepath, 'r') as f:
                        lines = sum(1 for _ in f)
                    lines -= 1  # Subtract header

                    data_files[f"{symbol}_{timeframe}"] = {
                        'filename': filename,
                        'symbol': symbol,
                        'timeframe': timeframe,
                        'rows': lines,
                        'size_kb': round(file_size / 1024, 1)
                    }

        return jsonify({
            'status': 'success',
            'symbols': sorted(list(symbols)),
            'timeframes': sorted(list(timeframes)),
            'data_files': data_files
        })

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Failed to load data options: {str(e)}'
        }), 500

@app.route('/api/data/files', methods=['GET'])
def get_data_files():
    """
    Return available CSV data files (legacy endpoint).
    """
    try:
        data_files_dir = os.path.join(os.path.dirname(__file__), 'data_files')
        if not os.path.exists(data_files_dir):
            return jsonify({
                'status': 'error',
                'message': 'Data files directory not found'
            }), 404

        files = []
        for filename in os.listdir(data_files_dir):
            if filename.endswith('.csv'):
                filepath = os.path.join(data_files_dir, filename)
                # Get basic file info
                file_size = os.path.getsize(filepath)
                # Count lines (rough estimate of data points)
                with open(filepath, 'r') as f:
                    lines = sum(1 for _ in f)
                lines -= 1  # Subtract header

                files.append({
                    'name': filename,
                    'symbol': filename.replace('_1h.csv', '').replace('_1d.csv', ''),
                    'rows': lines,
                    'size_kb': round(file_size / 1024, 1)
                })

        return jsonify({
            'status': 'success',
            'files': files
        })

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Failed to list data files: {str(e)}'
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """
    Health check endpoint.
    """
    return jsonify({
        'status': 'healthy',
        'message': 'Backtester API is running'
    })

# SocketIO event handlers for streaming backtest

@socketio.on('start_backtest')
def handle_start_backtest(data):
    session_id = request.sid
    
    try:
        # Validate required parameters
        required = ['symbol', 'strategy', 'strategy_params', 'initial_cash', 'csv_file']
        for req in required:
            if req not in data:
                emit('error', {'message': f'Missing required parameter: {req}'})
                return

        # Initialize components
        csv_path = os.path.join(os.path.dirname(__file__), 'data_files', data['csv_file'])
        if not os.path.exists(csv_path):
            emit('error', {'message': f'CSV file not found: {data["csv_file"]}'})
            return

        handler = DataHandler(csv_path)
        event_queue = EventQueue()
        exec_handler = ExecutionHandler()
        portfolio = Portfolio(data['initial_cash'])

        # Create strategy
        strategy_name = data['strategy']
        if strategy_name == 'sma':
            strategy = SMA_Crossover_Strategy(
                data['symbol'],
                handler,
                event_queue,
                **data['strategy_params']
            )
        elif strategy_name == 'rsi':
            strategy = RSI_Strategy(
                data['symbol'],
                handler,
                event_queue,
                **data['strategy_params']
            )
        else:
            emit('error', {'message': f'Unknown strategy: {strategy_name}'})
            return

        # Store session
        backtest_sessions[session_id] = {
            'handler': handler,
            'event_queue': event_queue,
            'strategy': strategy,
            'portfolio': portfolio,
            'exec_handler': exec_handler,
            'is_playing': False,
            'current_index': 0,
            'equity_curve': [],
            'trade_log': [],
            'bars': []
        }

        # Emit initial state
        emit('backtest_started', {
            'initial_cash': data['initial_cash'],
            'symbol': data['symbol'],
            'strategy': strategy_name,
            'total_bars': len(handler.data)
        })

    except Exception as e:
        emit('error', {'message': f'Failed to start backtest: {str(e)}'})

@socketio.on('play')
def handle_play():
    session_id = request.sid
    print(f"Received play event from session {session_id}")
    if session_id not in backtest_sessions:
        emit('error', {'message': 'No active backtest session'})
        return
    
    session = backtest_sessions[session_id]
    if session['is_playing']:
        return  # Already playing
    
    session['is_playing'] = True
    socketio.start_background_task(play_backtest, session_id)

@socketio.on('pause')
def handle_pause():
    session_id = request.sid
    print(f"Received pause event from session {session_id}")
    if session_id in backtest_sessions:
        backtest_sessions[session_id]['is_playing'] = False

@socketio.on('step_forward')
def handle_step_forward():
    session_id = request.sid
    print(f"Received step_forward event from session {session_id}")
    if session_id not in backtest_sessions:
        emit('error', {'message': 'No active backtest session'})
        return
    
    session = backtest_sessions[session_id]
    process_next_bar(session, session_id)

@socketio.on('reset')
def handle_reset():
    session_id = request.sid
    print(f"Received reset event from session {session_id}")
    if session_id in backtest_sessions:
        del backtest_sessions[session_id]
        emit('backtest_reset')

def play_backtest(session_id):
    session = backtest_sessions.get(session_id)
    if not session:
        return
    
    while session['is_playing'] and session['handler'].has_next():
        process_next_bar(session, session_id)
        time.sleep(0.1)  # Simulate real-time delay (adjust as needed)
    
    session['is_playing'] = False
    emit('backtest_finished', room=session_id)

def process_next_bar(session, session_id):
    if not session['handler'].has_next():
        return
    
    bar = session['handler'].get_next_bar()
    session['bars'].append(bar)
    session['current_index'] += 1
    
    # Process the bar through the strategy
    market_event = MarketEvent(bar)
    session['event_queue'].put(market_event)
    
    while not session['event_queue'].empty():
        ev = session['event_queue'].get()
        if ev.type == "MARKET":
            session['strategy'].on_market_event(ev.bar)
        elif ev.type == "SIGNAL":
            order = session['portfolio'].update_signal(ev)
            if order:
                fill = session['exec_handler'].execute_order(order, bar["close"])
                session['portfolio'].update_fill(fill)
                session['trade_log'].append({
                    'timestamp': bar['timestamp'],
                    'type': fill.fill_type,
                    'price': fill.price,
                    'quantity': fill.quantity
                })
    
    # Update equity curve
    session['equity_curve'].append({
        'timestamp': bar['timestamp'],
        'equity': session['portfolio'].equity
    })
    
    # Emit update
    emit('bar_update', {
        'bar': bar,
        'equity': session['portfolio'].equity,
        'cash': session['portfolio'].cash,
        'positions': session['portfolio'].positions,
        'trade_log': session['trade_log'][-1] if session['trade_log'] else None
    }, room=session_id)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print("Starting Backtester API server with SocketIO...")
    print("Available endpoints:")
    print("  POST /api/backtest - Run a backtest")
    print("  GET  /api/strategies - List available strategies")
    print("  GET  /api/data/files - List available data files")
    print("  GET  /api/health - Health check")
    print("  WebSocket events: start_backtest, play, pause, step_forward, reset")
    print(f"\nServer will be available at http://localhost:{port}")
    socketio.run(app, debug=False, host='0.0.0.0', port=port)