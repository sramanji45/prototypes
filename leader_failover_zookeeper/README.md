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
CONTAINER ID   IMAGE           COMMAND                  CREATED         STATUS         PORTS                                         NAMES
6a40bcd10c09   build-worker    "python leader_failo…"   4 seconds ago   Up 3 seconds                                                 build-worker-2
a1200058cd88   build-worker    "python leader_failo…"   4 seconds ago   Up 3 seconds                                                 build-worker-1
ea2273cf68f8   zookeeper:3.8   "/docker-entrypoint.…"   2 hours ago     Up 2 hours     0.0.0.0:2181->2181/tcp, [::]:2181->2181/tcp   build-zookeeper-1
```
### Who has become the leader
```aiignore
worker-2  | Connected to ZooKeeper!
worker-2  | Aspring to become leader:6a40bcd10c09
worker-2  | I am the Leader:6a40bcd10c09
worker-1  | Connected to ZooKeeper!
worker-1  | Aspring to become leader:a1200058cd88
worker-1  | Leader is elected already. Standing by:a1200058cd88
worker-1  | Watching Leader...
```
#### Connect to Zookeeper
```aiignore
$docker exec -it build-zookeeper-1 bash
root@5286a389a008:/apache-zookeeper-3.8.4-bin# zkCli.sh
[zk: localhost:2181(CONNECTED) 0] ls /
[leader, zookeeper]
[zk: localhost:2181(CONNECTED) 1] get /leader
6a40bcd10c09
[zk: localhost:2181(CONNECTED) 2] stat /leader
cZxid = 0xb
ctime = Fri Jan 02 14:45:01 UTC 2026
mZxid = 0xb
mtime = Fri Jan 02 14:45:01 UTC 2026
pZxid = 0xb
cversion = 0
dataVersion = 0
aclVersion = 0
ephemeralOwner = 0x10000392c530003
dataLength = 12
numChildren = 0
[zk: localhost:2181(CONNECTED) 3] quit
```
### Stop the Leader
```aiignore
$docker stop 6a40bcd10c09
6a40bcd10c09

$docker ps
CONTAINER ID   IMAGE           COMMAND                  CREATED         STATUS         PORTS                                         NAMES
a1200058cd88   build-worker    "python leader_failo…"   4 minutes ago   Up 4 minutes                                                 build-worker-1
ea2273cf68f8   zookeeper:3.8   "/docker-entrypoint.…"   2 hours ago     Up 2 hours     0.0.0.0:2181->2181/tcp, [::]:2181->2181/tcp   build-zookeeper-1
```
### Did Re-election happen ? Yes
```aiignore
worker-2 exited with code 137
zookeeper-1  | 2026-01-02 14:48:31,344 [myid:] - INFO  [SessionTracker:o.a.z.s.ZooKeeperServer@643] - Expiring session 0x10000392c530003, timeout of 10000ms exceeded
worker-1     | Aspring to become leader:a1200058cd88
worker-1     | I am the Leader:a1200058cd88
```
### Getting the leader from zookeeper
```aiignore
[zk: localhost:2181(CONNECTED) 0] ls /
[leader, zookeeper]
[zk: localhost:2181(CONNECTED) 1] get /leader
a1200058cd88
[zk: localhost:2181(CONNECTED) 2] stat /leader
cZxid = 0x11
ctime = Fri Jan 02 14:48:31 UTC 2026
mZxid = 0x11
mtime = Fri Jan 02 14:48:31 UTC 2026
pZxid = 0x11
cversion = 0
dataVersion = 0
aclVersion = 0
ephemeralOwner = 0x10000392c530004
dataLength = 12
numChildren = 0
[zk: localhost:2181(CONNECTED) 3] quit
```
Worker-1 has become the leader, a1200058cd88 is container id for worker-1