from flask import Flask, jsonify

user_app = Flask(__name__)

# Mock database of users
USERS = {
    "1": {"name": "Alice", "role": "Developer"},
    "2": {"name": "Bob", "role": "Architect"}
}

@user_app.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    print(user_id)
    if user_id in USERS:
        return jsonify(USERS[user_id])
    return jsonify({"error": "User not found"}), 404

if __name__ == '__main__':
    # We run the backend service on a different port
    user_app.run(port=5003)