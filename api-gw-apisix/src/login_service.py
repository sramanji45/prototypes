import jwt
import time
from flask import Flask, jsonify, request

login_app = Flask(__name__)

# 1. These must match exactly what you put in the APISIX Consumer
SECRET_KEY = "your-ultra-secure-shared-secret"
KEY_ID = "user-service-issuer"  # This matches the 'key' in APISIX


def generate_token(user_id, role):
    payload = {
        "iss": KEY_ID,  # Issuer (APISIX uses this to find the secret)
        "iat": int(time.time()),  # Issued At
        "exp": int(time.time()) + 3600,  # Expires in 1 hour
        "user_id": user_id,  # Custom data for your backend
        "role": role
    }
    # Generate the encoded JWT
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token

@login_app.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    return jsonify({"Token": generate_token(data['user_id'], "admin")})
if __name__ == '__main__':
    # We run the backend service on a different port
    login_app.run(port=5001)