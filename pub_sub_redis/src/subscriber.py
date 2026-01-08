import os
import redis
import time

# 1. Connect to Redis
redis_host = os.getenv("REDIS_HOST", "localhost")
redis_port = os.getenv("REDIS_PORT", "6379")
client = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)

# 2. Create a pubsub object
pubsub = client.pubsub()

# 3. Subscribe to channels
channels = ["redis_prototype"]
for channel in channels:
    pubsub.subscribe(channel)

print(f"Listening on {channels}... Press Ctrl+C to stop.")

# 4. The Message Loop
try:
    for message in pubsub.listen():
        if message['type'] == 'message':
            print(f"Received:{message['data']} from {message['channel']}")
        elif message['type'] == 'subscribe':
            print(f"Subscribed to :{message['channel']}")
except KeyboardInterrupt:
    print("\nStopping subscriber...")