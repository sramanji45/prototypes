from flask import Flask, request, jsonify, redirect
import requests
app = Flask(__name__)

# --- Service Mapping ---
SERVICE_MAP = {
    '/users': 'http://localhost:5001', # User Service URL
    "/login": "http://localhost:5002" # User Login Service
    # We could add more here, like: '/products': 'http://localhost:5002'
}
# -----------------------
# The secret key we expect from the client
EXPECTED_API_KEY = "super-secret-key-123"
LOGIN_URL = "http://localhost:5002/login" #"http://your-frontend-app.com/login" # The actual login page URL

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE'])
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def catch_all(path):
    # --- 1. AUTHENTICATION MIDDLEWARE ---
    # Look for the 'X-Api-Key' header in the incoming request
    client_api_key = request.headers.get('X-Api-Key')
    is_authenticated = (client_api_key == EXPECTED_API_KEY)  # Replace with actual token validation

    if not is_authenticated:
        # Check if the request likely came from a web browser (e.g., expects HTML)
        # This is a simple check; real-world apps use more robust methods.
        print(request.headers)
        if not request.headers.get('Accept', ''):
            # If it looks like a browser, redirect the user to the login page
            print("Redirecting the user to the login page")
            return redirect(LOGIN_URL, code=302)  # 302 Found is a common temporary redirect
        else:
            # If it looks like an API call (e.g., expecting JSON), return 401
            return jsonify({
                "error": "Unauthorized",
                "message": "Missing or invalid API Key/Token."
            }), 401
    # ----------------------------

    target_url = None
    for prefix, base_url in SERVICE_MAP.items():
        if path.startswith(prefix.strip('/')):
            target_url = base_url + "/" + path
            break
    print(target_url)
    if target_url is None:
        return jsonify({"error": "Service not found for this path"}), 404

    # Forward the request to the target service
    try:
        headers = dict(request.headers)
        method = request.method
        data = request.get_data()
        resp = requests.request(method, target_url,
                                headers=headers, data=data, params=request.args, timeout=5)
        # 3. Return the response back to the client
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        headers = [(name, value) for name, value in resp.raw.headers.items() if name.lower() not in excluded_headers]

        return resp.content, resp.status_code, headers
    except requests.exceptions.RequestException as e:
        # Handle connection errors (e.g., if the backend service is down)
        print(f"Error forwarding request: {e}")
        return jsonify({"error": "Gateway could not connect to the upstream service"}), 503
    except Exception as ex:
        return jsonify({"error": str(ex)}), 400

    return jsonify({"gateway_status": "Up", "requested_path": path})


if __name__ == '__main__':
    app.run(port=5000)