from flask import Flask, jsonify, request
from flask_cors import CORS
import jwt
import datetime
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:5173", "http://localhost:5174", "http://127.0.0.1:5173", "http://127.0.0.1:5174"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization", "Accept"],
        "expose_headers": ["Content-Type", "Authorization"],
        "supports_credentials": True
    }
})

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

        # Check if user already exists
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

        # Check if user exists
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
    app.run(host='0.0.0.0', port=5002)