@echo off
cd c:\Users\Abochi\Desktop\backtester\backend
python -c "
from flask import Flask, jsonify, request
from flask_cors import CORS
import jwt
import datetime
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
CORS(app, resources={
    r'/api/*': {
        'origins': ['http://localhost:5173', 'http://localhost:5174', 'http://localhost:5175'],
        'methods': ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
        'allow_headers': ['Content-Type', 'Authorization', 'Accept'],
        'expose_headers': ['Content-Type', 'Authorization'],
        'supports_credentials': True
    }
})

app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
users = {}

@app.route('/api/test', methods=['GET', 'OPTIONS'])
def test_cors():
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    return jsonify({'message': 'CORS test successful', 'status': 'ok'}), 200

@app.route('/api/auth/register', methods=['POST', 'OPTIONS'])
def register():
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    
    try:
        data = request.get_json()
        if not data or not all(k in data for k in ['email', 'password', 'name']):
            return jsonify({'error': 'Missing required fields'}), 400

        email = data['email'].lower()
        if email in users:
            return jsonify({'error': 'User already exists'}), 409

        user_id = str(len(users) + 1)
        users[email] = {
            'id': user_id,
            'email': email,
            'name': data['name'],
            'password_hash': generate_password_hash(data['password']),
            'created_at': datetime.datetime.utcnow().isoformat()
        }

        token = jwt.encode({
            'user_id': user_id,
            'email': email,
            'name': data['name'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7)
        }, app.config['SECRET_KEY'], algorithm='HS256')

        return jsonify({
            'token': token,
            'user': {
                'id': user_id,
                'email': email,
                'name': data['name']
            }
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/auth/login', methods=['POST', 'OPTIONS'])
def login():
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    
    try:
        data = request.get_json()
        if not data or not all(k in data for k in ['email', 'password']):
            return jsonify({'error': 'Missing email or password'}), 400

        email = data['email'].lower()
        if email not in users:
            return jsonify({'error': 'Invalid credentials'}), 401

        user = users[email]
        if not check_password_hash(user['password_hash'], data['password']):
            return jsonify({'error': 'Invalid credentials'}), 401

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

if __name__ == '__main__':
    print('Starting Backtester API server on port 5002...')
    app.run(host='0.0.0.0', port=5002, debug=False, use_reloader=False)
"