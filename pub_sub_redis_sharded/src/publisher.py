import redis
import hashlib

class ShardedRedisPubSub:
    def __init__(self, redis_instances):
        self.redis_instances = redis_instances
        self.num_shards = len(redis_instances)

    def get_shard_index(self, channel):
        #CRC16 calculation which is used by Redis
        hash_value = int(hashlib.md5(channel.encode()).hexdigest(), 16)
        return hash_value % self.num_shards

    def publish(self, channel, message):
        shard_index = self.get_shard_index(channel)
        redis_instance = self.redis_instances[shard_index]
        return redis_instance.publish(channel, message)


redis_instances = [ redis.Redis(host='redis-node-1', port=6379),
                    redis.Redis(host='redis-node-2', port=6379),
                    redis.Redis(host='redis-node-3', port=6379) ]
sharded_pubsub = ShardedRedisPubSub(redis_instances)
sharded_pubsub.publish('orders', 'New Order 1')
sharded_pubsub.publish('sensors', 'New Sensors Data 1')
