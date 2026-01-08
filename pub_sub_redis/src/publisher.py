import os
import redis
import time

# 1. Connect to Redis
redis_host = os.getenv("REDIS_HOST", "localhost")
redis_port = os.getenv("REDIS_PORT", "6379")
client = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)

# 2. Create a pubsub object
pubsub = client.pubsub()

# 3. Run the input loop
channel = "redis_prototype"
while True:
    print("Enter one of the following options:")
    print("1. Publish one message")
    print("2. Publish N messages")
    print("3. Exit")
    option = input()
    if option == "1":
        message = input("Enter message to send: ")
        client.publish(channel, message.encode("utf-8"))
    elif option == "2":
        num = input("How many messages to send?")
        for i in range(int(num)):
            message = f"test_{i}"
            client.publish(channel, message.encode("utf-8"))
    elif option == "3":
        exit(0)
