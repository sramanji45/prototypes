### Build Docker images
```
$cd prototypes/pub_sub_redis/build
$docker compose --verbose build
```

### Run the containers
```aiignore
$docker compose up -d 
[+] Running 3/3
 ✔ Network build_redis-pubsub-net  Created                                                                                                                      0.0s 
 ✔ Container redis-proto           Started                                                                                                                      0.1s 
 ✔ Container app-sub               Started                                                                                                                      0.1s 
```

### Check Container are running fine or not
```aiignore
$docker ps
CONTAINER ID   IMAGE              COMMAND                  CREATED         STATUS         PORTS                                         NAMES
d9abf6c50fbe   redis:7.2-alpine   "docker-entrypoint.s…"   2 minutes ago   Up 2 minutes   0.0.0.0:6379->6379/tcp, [::]:6379->6379/tcp   redis-proto
3ff1a7bbe9b8   build-app          "python subscriber.py"   2 minutes ago   Up 2 minutes                                                 app-sub

$docker compose logs -f
app-sub  | Listening on ['redis_prototype']... Press Ctrl+C to stop.
app-sub  | {'type': 'subscribe', 'pattern': None, 'channel': 'redis_prototype', 'data': 1}
redis-proto  | 1:C 08 Jan 2026 17:04:20.734 * oO0OoO0OoO0Oo Redis is starting oO0OoO0OoO0Oo
redis-proto  | 1:C 08 Jan 2026 17:04:20.734 * Redis version=7.2.12, bits=64, commit=00000000, modified=0, pid=1, just started
redis-proto  | 1:C 08 Jan 2026 17:04:20.734 # Warning: no config file specified, using the default config. In order to specify a config file use redis-server /path/to/redis.conf
redis-proto  | 1:M 08 Jan 2026 17:04:20.735 * monotonic clock: POSIX clock_gettime
redis-proto  | 1:M 08 Jan 2026 17:04:20.735 * Running mode=standalone, port=6379.
redis-proto  | 1:M 08 Jan 2026 17:04:20.736 * Server initialized
redis-proto  | 1:M 08 Jan 2026 17:04:20.736 * Loading RDB produced by version 7.2.12
redis-proto  | 1:M 08 Jan 2026 17:04:20.736 * RDB age 20 seconds
redis-proto  | 1:M 08 Jan 2026 17:04:20.736 * RDB memory usage when created 0.93 Mb
redis-proto  | 1:M 08 Jan 2026 17:04:20.736 * Done loading RDB, keys loaded: 0, keys expired: 0.
redis-proto  | 1:M 08 Jan 2026 17:04:20.736 * DB loaded from disk: 0.000 seconds
redis-proto  | 1:M 08 Jan 2026 17:04:20.736 * Ready to accept connections tcp
```

### Run Publisher and Send messages
```aiignore
$docker exec -it app-sub bash
root@ffded5e74b3a:/app# python publisher.py 
Enter one of the following options:
1. Publish one message
2. Publish N messages
3. Exit
1
Enter message to send: Hello World!
Enter one of the following options:
1. Publish one message
2. Publish N messages
3. Exit
2
How many messages to send?10
Enter one of the following options:
1. Publish one message
2. Publish N messages
3. Exit

```
### Check Subscriber logs
```aiignore
app-sub      | Received: Hello World! from redis_prototype
app-sub      | Received: test_0 from redis_prototype
app-sub      | Received: test_1 from redis_prototype
app-sub      | Received: test_2 from redis_prototype
app-sub      | Received: test_3 from redis_prototype
app-sub      | Received: test_4 from redis_prototype
app-sub      | Received: test_5 from redis_prototype
app-sub      | Received: test_6 from redis_prototype
app-sub      | Received: test_7 from redis_prototype
app-sub      | Received: test_8 from redis_prototype
app-sub      | Received: test_9 from redis_prototype
```