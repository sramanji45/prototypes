import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    # Showing which instance is responding
    instance_name = os.getenv('INSTANCE_NAME', 'Unknown')
    return f"Hello from {instance_name}!"

if __name__ == "__main__":
    # The host '0.0.0.0' makes the app accessible outside the container's localhost
    app.run(host='0.0.0.0', port=5000)