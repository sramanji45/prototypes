# user_service.py
from flask import Flask, jsonify, request

login_app = Flask(__name__)

# Mock database of users
USERS = {
    "1": {"name": "Alice", "role": "Developer"},
    "2": {"name": "Bob", "role": "Architect"}
}

@login_app.route('/login', methods=['GET', 'PUT', 'POST'])
def login():
    headers = request.headers
    """
    user_id = headers.get('X-User-Id')
    if user_id not in USERS:
        return jsonify({"error": "User not found"}), 404
    """
    #Login is pass
    return jsonify({"Token": "super-secret-key-123"})
if __name__ == '__main__':
    # We run the backend service on a different port
    login_app.run(port=5002)