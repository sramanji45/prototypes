import os
from flask import Flask
from cache import get_cached_data, simulate_expensive_db_call

app = Flask(__name__)

@app.route('/')
def hello():
    instance_name = os.getenv('INSTANCE_NAME', 'Unknown')
    return f"Hello from {instance_name}!"


@app.get("/kv/{key}")
async def get_key(key: str):
     data = await get_cached_data(f"item:{key}", simulate_expensive_db_call)
     return data


if __name__ == "__main__":
    # The host '0.0.0.0' makes the app accessible outside the container's localhost
    app.run(host='0.0.0.0', port=5000)