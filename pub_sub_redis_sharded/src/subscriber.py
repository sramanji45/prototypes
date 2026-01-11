import redis
import hashlib
import threading
import signal
import sys

def orders_callback(message):
    print(f"Orders Data Received:{message['data']} from {message['channel']}")

def sensors_callback(message):
    print(f"Sensors Data Received:{message['data']} from {message['channel']}")

class ShardedRedisPubSub:
    def __init__(self, redis_instances):
        self.redis_instances = redis_instances
        self.num_shards = len(redis_instances)
        self.threads = []
        self.stop_event = threading.Event()  # The "Kill Switch"

    def get_shard_index(self, channel):
        #CRC16 calculation
        hash_value = int(hashlib.md5(channel.encode()).hexdigest(), 16)
        return hash_value % self.num_shards

    def publish(self, channel, message):
        shard_index = self.get_shard_index(channel)
        redis_instance = self.redis_instances[shard_index]
        return redis_instance.publish(channel, message)

    def subscribe(self, channels, callbacks):
        pubsubs = []
        for i, redis_instance in enumerate(self.redis_instances):
            shard_channels = [ch for ch in channels if self.get_shard_index(ch) == i]
            for shard_channel in shard_channels:
                callback = callbacks[shard_channel]
                pubsub = redis_instance.pubsub()
                pubsub.subscribe(shard_channel)
                print(f"Subscribed to {shard_channel} on {self.redis_instances[i]}")
                pubsubs.append(pubsub)
                thread = threading.Thread(target=self._listen_thread, args=(pubsub, callback), daemon=True)
                thread.start()
                self.threads.append(thread)
        return pubsubs

    def _listen_thread(self, pubsub, callback):
        print(f"Listening on {pubsub}")
        while not self.stop_event.is_set():
            for message in pubsub.listen():
                if message['type'] == 'message':
                    callback(message)
        pubsub.close()
        print("Thread cleaned up and closed.")

    def wait_for_completion(self):
        """Blocks the main thread until all shard threads exit"""
        try:
            for thread in self.threads:
                if thread.is_alive():
                    thread.join()
        except (KeyboardInterrupt, SystemExit):
            self.stop()  # Trigger the cleanup

    def stop(self):
        print("\nStopping threads gracefully...")
        self.stop_event.set()  # Tell threads to stop
        for thread in self.threads:
            thread.join()  # Wait for them to finish their current loop


def signal_handler(sig, frame):
    print("\nReceived STOP signal, Shutting down gracefully...")
    sharded_pubsub.stop()
    sys.exit(0)

# Register the signal handlers
signal.signal(signal.SIGINT, signal_handler)  # Catch Ctrl+C
signal.signal(signal.SIGTERM, signal_handler) # Catch Docker Stop

callbacks = {
    "orders": orders_callback,
    "sensors": sensors_callback
}
redis_instances = [ redis.Redis(host='redis-node-1', port=6379),
                    redis.Redis(host='redis-node-2', port=6379),
                    redis.Redis(host='redis-node-3', port=6379)]
sharded_pubsub = ShardedRedisPubSub(redis_instances)
sharded_pubsub.subscribe(callbacks.keys(), callbacks)
sharded_pubsub.wait_for_completion()
sharded_pubsub.wait_for_completion()
