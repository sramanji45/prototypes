### Redis Sharding
When we use Sharded Pub/Sub, Redis uses an algorithm called CRC16 to turn your channel name into a number between 0 and 16383.

When looks like Redis doesnt provide a way to change this hashing algorithm for good reasons. 
Redis client also uses the same algorithm to identify the node in the cluster

### How does client reads/writes from appropriate node ?
1. Redis Client connects to one of the nodes and sends a special command called CLUSTER SLOTS
```aiignore
client = RedisCluster(startup_nodes=startup_nodes, decode_responses=True)
```
2. Redis node replies with "metadata" of the cluster:
```aiignore
"Node A (172.18.0.2) owns slots 0-8191"
"Node B (172.18.0.3) owns slots 8192-16383"
```
3. The client caches (remembers) this map locally in its memory.

When you try to publish to a channel like "my_sharded_channel", the client runs the CRC16 math locally. It sees that the channel belongs to slot 5000. It looks at its cached map, sees that Node A owns slot 5000, and sends the request directly there.

### What happens if the cluster changes
1. The client sends the request to Node A.
2. Node A realizes, "Hey, I don't own slot 5000 anymore, Node B does!"
3. Node A sends back a specific error: -MOVED 5000 172.18.0.3:6379.
4. The client says "Oops!", updates its local map, and automatically retries the request with Node B.

### Check the containers
```aiignore
$docker ps
CONTAINER ID   IMAGE              COMMAND                  CREATED          STATUS          PORTS                                         NAMES
59df0d7a6ed5   build-app          "python subscriber.py"   11 seconds ago   Up 11 seconds                                                 app-sub
5a204f7d5f02   redis:7.2-alpine   "docker-entrypoint.s…"   11 minutes ago   Up 11 minutes   0.0.0.0:6372->6379/tcp, [::]:6372->6379/tcp   redis-node-2
e2b7cd8df370   redis:7.2-alpine   "docker-entrypoint.s…"   11 minutes ago   Up 11 minutes   0.0.0.0:6373->6379/tcp, [::]:6373->6379/tcp   redis-node-3
8589faba480b   redis:7.2-alpine   "docker-entrypoint.s…"   11 minutes ago   Up 11 minutes   0.0.0.0:6371->6379/tcp, [::]:6371->6379/tcp   redis-node-1
```

### Create redis cluster
```aiignore
$docker exec -it redis-node-1 redis-cli --cluster create redis-node-1:6379 redis-node-2:6379 redis-node-3:6379 --cluster-replicas 0 --cluster-yes
>>> Performing hash slots allocation on 3 nodes...
Master[0] -> Slots 0 - 5460
Master[1] -> Slots 5461 - 10922
Master[2] -> Slots 10923 - 16383
M: 777beb9c0bb0ed103494484770fd0168ab4cad0f redis-node-1:6379
   slots:[0-5460] (5461 slots) master
M: 43936e78e1ccc9ad4ba6d25c23f31ffe3b11e069 redis-node-2:6379
   slots:[5461-10922] (5462 slots) master
M: 9f00ab9f8a3a405c053e187c00dd7838b09858a7 redis-node-3:6379
   slots:[10923-16383] (5461 slots) master
>>> Nodes configuration updated
>>> Assign a different config epoch to each node
>>> Sending CLUSTER MEET messages to join the cluster
Waiting for the cluster to join
.
>>> Performing Cluster Check (using node redis-node-1:6379)
M: 777beb9c0bb0ed103494484770fd0168ab4cad0f redis-node-1:6379
   slots:[0-5460] (5461 slots) master
M: 43936e78e1ccc9ad4ba6d25c23f31ffe3b11e069 172.20.0.4:6379
   slots:[5461-10922] (5462 slots) master
M: 9f00ab9f8a3a405c053e187c00dd7838b09858a7 172.20.0.2:6379
   slots:[10923-16383] (5461 slots) master
[OK] All nodes agree about slots configuration.
>>> Check for open slots...
>>> Check slots coverage...
[OK] All 16384 slots covered.
```

### Rebuild and create the app container
```aiignore
$docker-compose up -d --build app
```
### Calculate the channel hash
```aiignore
$docker exec -it redis-node-1 redis-cli CLUSTER KEYSLOT orders
(integer) 105
$docker exec -it redis-node-1 redis-cli CLUSTER KEYSLOT sensors
(integer) 6322
```

### Check the Cluster Nodes and Partitions
```aiignore
$docker exec -it redis-node-1 redis-cli CLUSTER NODES
43936e78e1ccc9ad4ba6d25c23f31ffe3b11e069 172.20.0.4:6379@16379 master - 0 1768129310375 2 connected 5461-10922
777beb9c0bb0ed103494484770fd0168ab4cad0f 172.20.0.5:6379@16379 myself,master - 0 1768129307000 1 connected 0-5460
9f00ab9f8a3a405c053e187c00dd7838b09858a7 172.20.0.2:6379@16379 master - 0 1768129309331 3 connected 10923-16383
```

### Monitor publishing message
```aiignore
$docker exec -it redis-node-1 redis-cli MONITOR
OK
1768129067.601166 [0 172.20.0.3:39622] "CLIENT" "SETINFO" "LIB-NAME" "redis-py"
1768129067.601225 [0 172.20.0.3:39622] "CLIENT" "SETINFO" "LIB-VER" "7.0.1"
1768129067.601730 [0 172.20.0.3:39622] "COMMAND"
1768129077.999131 [0 172.20.0.3:39622] "SPUBLISH" "orders" "Order1"
```
### Verify subscription status
```aiignore
$docker exec -it redis-node-1 redis-cli PUBSUB SHARDNUMSUB orders
1) "orders"
2) (integer) 1
```

### Clear all redis data when we bring down and bring up redis nodes
```aiignore
docker exec -it redis-node-1 redis-cli FLUSHALL
docker exec -it redis-node-1 redis-cli CLUSTER RESET HARD
docker exec -it redis-node-2 redis-cli FLUSHALL
docker exec -it redis-node-2 redis-cli CLUSTER RESET HARD
docker exec -it redis-node-3 redis-cli FLUSHALL
docker exec -it redis-node-3 redis-cli CLUSTER RESET HARD
```

### Publish data to Channels
```aiignore
$docker exec -it app-sub bash
root@a058cccd2ac8:/app# python publisher.py
```

### Verify Consuming from Channels
```aiignore
app-sub has been recreated
app-sub       | Subscribed to orders on <redis.client.Redis(<redis.connection.ConnectionPool(<redis.connection.Connection(db=0,username=None,password=None,socket_timeout=None,encoding=utf-8,encoding_errors=strict,decode_responses=False,retry_on_error=[],retry=<redis.retry.Retry object at 0xffff812ced50>,health_check_interval=0,client_name=None,lib_name=redis-py,lib_version=7.0.1,redis_connect_func=None,credential_provider=None,protocol=2,host=redis-node-2,port=6379,socket_connect_timeout=None,socket_keepalive=None,socket_keepalive_options=None)>)>)>
app-sub       | Listening on <redis.client.PubSub object at 0xffff812d84d0>
app-sub       | Subscribed to sensors on <redis.client.Redis(<redis.connection.ConnectionPool(<redis.connection.Connection(db=0,username=None,password=None,socket_timeout=None,encoding=utf-8,encoding_errors=strict,decode_responses=False,retry_on_error=[],retry=<redis.retry.Retry object at 0xffff812d5910>,health_check_interval=0,client_name=None,lib_name=redis-py,lib_version=7.0.1,redis_connect_func=None,credential_provider=None,protocol=2,host=redis-node-3,port=6379,socket_connect_timeout=None,socket_keepalive=None,socket_keepalive_options=None)>)>)>
app-sub       | Listening on <redis.client.PubSub object at 0xffff812d9410>

app-sub       | Orders Data Received:b'New Order 1' from b'orders'
app-sub       | Sensors Data Received:b'New Sensors Data 1' from b'sensors'
```

### Stop the app
```aiignore
app-sub       | 
app-sub       | Received STOP signal, Shutting down gracefully...
app-sub       | 
app-sub       | Stopping threads gracefully...
app-sub exited with code 137
```