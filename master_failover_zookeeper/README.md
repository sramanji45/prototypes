### Bring up all the containers
```aiignore
$docker commpose --verbose up -d
[+] Running 5/5
 ✔ build-worker                 Built                                                                                                                           0.0s 
 ✔ Network build_default        Created                                                                                                                         0.0s 
 ✔ Container build-zookeeper-1  Started                                                                                                                         0.2s 
 ✔ Container build-worker-2     Started                                                                                                                         0.3s 
 ✔ Container build-worker-1     Started
```
### Ensure all the containers are running
```aiignore
$docker ps 
CONTAINER ID   IMAGE           COMMAND                  CREATED          STATUS          PORTS                                         NAMES
bf016d6f02a5   build-worker    "python master_failo…"   40 seconds ago   Up 39 seconds                                                 build-worker-2
9b4cb647d4f6   build-worker    "python master_failo…"   40 seconds ago   Up 39 seconds                                                 build-worker-1
97ffe9297cb8   zookeeper:3.8   "/docker-entrypoint.…"   40 seconds ago   Up 39 seconds   0.0.0.0:2181->2181/tcp, [::]:2181->2181/tcp   build-zookeeper-1
```
### Who has become the master
```aiignore
worker-1  | Connection dropped: socket connection error: Connection refused
worker-1  | Connected to ZooKeeper!
worker-1  | Aspring to become master:f868db2063d0
worker-1  | I am the Master:f868db2063d0
worker-2  | Connection dropped: socket connection error: Connection refused
worker-2  | Connection dropped: socket connection error: Connection refused
worker-2  | Connected to ZooKeeper!
worker-2  | Aspring to become master:021b0ee78fe6
worker-2  | Master is elected already. Standing by:021b0ee78fe6
worker-2  | Watching Master...
```
#### Connect to Zookeeper
```aiignore
$docker exec -it build-zookeeper-1 bash
root@5286a389a008:/apache-zookeeper-3.8.4-bin# zkCli.sh
[zk: localhost:2181(CONNECTED) 0] ls /
[master, zookeeper]
[zk: localhost:2181(CONNECTED) 1] get /master
f868db2063d0
[zk: localhost:2181(CONNECTED) 2] stat /master
cZxid = 0x4
ctime = Fri Jan 02 12:28:38 UTC 2026
mZxid = 0x4
mtime = Fri Jan 02 12:28:38 UTC 2026
pZxid = 0x4
cversion = 0
dataVersion = 0
aclVersion = 0
ephemeralOwner = 0x100002b2de40000
dataLength = 12
numChildren = 0
[zk: localhost:2181(CONNECTED) 3] quit
```
### Stop the Master
```aiignore
$docker stop build-worker-1
build-worker-1

$docker ps
CONTAINER ID   IMAGE           COMMAND                  CREATED         STATUS         PORTS                                         NAMES
021b0ee78fe6   build-worker    "python master_failo…"   4 minutes ago   Up 4 minutes                                                 build-worker-2
ea2273cf68f8   zookeeper:3.8   "/docker-entrypoint.…"   4 minutes ago   Up 4 minutes   0.0.0.0:2181->2181/tcp, [::]:2181->2181/tcp   build-zookeeper-1
```
### Did Re-election happen ? Yes
```aiignore
worker-1 exited with code 137

zookeeper-1  | 2026-01-02 12:31:17,463 [myid:] - INFO  [SessionTracker:o.a.z.s.ZooKeeperServer@643] - Expiring session 0x10000392c530000, timeout of 10000ms exceeded
worker-2     | Aspring to become master:021b0ee78fe6
worker-2     | I am the Master:021b0ee78fe6
```
### Getting the master from zookeeper
```aiignore
[zk: localhost:2181(CONNECTED) 0] ls /
[master, zookeeper]
[zk: localhost:2181(CONNECTED) 1] get /master
021b0ee78fe6
[zk: localhost:2181(CONNECTED) 2] stat /master
cZxid = 0x6
ctime = Fri Jan 02 12:31:17 UTC 2026
mZxid = 0x6
mtime = Fri Jan 02 12:31:17 UTC 2026
pZxid = 0x6
cversion = 0
dataVersion = 0
aclVersion = 0
ephemeralOwner = 0x10000392c530001
dataLength = 12
numChildren = 0
[zk: localhost:2181(CONNECTED) 3] quit

WATCHER::

WatchedEvent state:Closed type:None path:null
2026-01-02 12:34:34,195 [myid:] - INFO  [main-EventThread:o.a.z.ClientCnxn$EventThread@569] - EventThread shut down for session: 0x10000392c530002
2026-01-02 12:34:34,195 [myid:] - INFO  [main:o.a.z.ZooKeeper@1232] - Session: 0x10000392c530002 closed
2026-01-02 12:34:34,197 [myid:] - INFO  [main:o.a.z.u.ServiceUtils@45] - Exiting JVM with code 0
```
Worker-2 has become the master, 021b0ee78fe6 is container id for worker-2