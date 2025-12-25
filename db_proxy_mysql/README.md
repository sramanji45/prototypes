### Setup MySQL master replica
```
cd mysql_master_replica/build
(.venv) ######@#####-MacBook-Pro build % docker-compose up -d 
[+] Running 4/4
 ✔ Network build_default     Created                                                                                                                            0.0s 
 ✔ Container mysql-master    Started                                                                                                                            0.1s 
 ✔ Container mysql-replica2  Started                                                                                                                    0.2s 
 ✔ Container mysql-replica1  Started                                                                                                                            0.1s 
(.venv) ####@####-MacBook-Pro build % docker ps
CONTAINER ID   IMAGE         COMMAND                  CREATED          STATUS          PORTS                                         NAMES
8e27d61e8f73   mysql:8.0.0   "docker-entrypoint.s…"   28 seconds ago   Up 28 seconds   0.0.0.0:3308->3306/tcp, [::]:3308->3306/tcp   mysql-replica2
597a7806c953   mysql:8.0.0   "docker-entrypoint.s…"   28 seconds ago   Up 28 seconds   0.0.0.0:3307->3306/tcp, [::]:3307->3306/tcp   mysql-replica1
f83e623b4ff9   mysql:8.0.0   "docker-entrypoint.s…"   28 seconds ago   Up 28 seconds   0.0.0.0:3306->3306/tcp, [::]:3306->3306/tcp   mysql-master
```
### List networks
```aiignore
docker network ls
```
### Create ProxySQL instance
```aiignore
cd db_proxy_mysql/build
docker-compose --verbose up -d
```
### Add monitoring user on replicas upon "Access denied" for monitoring user
```aiignore
sh add_monitoring_user.sh
```
### Check whether ProxySQL able to access MySQL servers
```aiignore
docker exec -it proxysql mysql -u admin -padmin -h 127.0.0.1 -P 6032 -e "SELECT * FROM monitor.mysql_server_connect_log ORDER BY time_start_us DESC LIMIT 5;"
+----------------+------+------------------+-------------------------+---------------+
| hostname       | port | time_start_us    | connect_success_time_us | connect_error |
+----------------+------+------------------+-------------------------+---------------+
| mysql-replica1 | 3306 | 1766667626151095 | 2296                    | NULL          |
| mysql-master   | 3306 | 1766667624721470 | 1681                    | NULL          |
| mysql-replica2 | 3306 | 1766667623293026 | 2119                    | NULL          |
| mysql-master   | 3306 | 1766667506286035 | 1542                    | NULL          |
| mysql-replica1 | 3306 | 1766667504787817 | 2938                    | NULL          |
+----------------+------+------------------+-------------------------+---------------+
```
### Create Database and Write Data to Master
```
docker exec -i mysql-master mysql -uroot -proot123 < write-to-master.sql
```
### Install the Library
```aiignore
pip install mysql-connector-python
```
### Perform Write and Read through ProxySQL
```aiignore
(.venv) #####@#####-MacBook-Pro db_proxy_mysql % python app.py 
--- Connected to ProxySQL ---

[Writing] Inserting new character...
Write successful!

[Reading] Fetching data from Replicas...
Data received from Server ID: 3
Name: Sathya Raj
```

## Failover
### Stop Master
```aiignore
docker stop  mysql-master
```
### ProxySQL logs
```aiignore
proxysql  | 2025-12-25 13:28:15 MySQL_Monitor.cpp:7392:monitor_ping_process_ready_task_thread(): [ERROR] Error after 0ms on server mysql-master:3306 : Lost connection to server during query
proxysql  | 2025-12-25 13:28:18 MySQL_Session.cpp:1616:handler_again___status_PINGING_SERVER(): [ERROR] Detected a broken connection while during ping on (10,mysql-master,3306,27) , FD (Conn:74 , MyDS:74) , user root , last_used 0ms ago : 2013, Lost connection to server during query
proxysql  | 2025-12-25 13:28:23 MySQL_Monitor.cpp:4780:monitor_dns_resolver_thread(): [ERROR] An error occurred while resolving hostname: mysql-master [-2]
proxysql  | 2025-12-25 13:28:39 MySQL_Monitor.cpp:3303:monitor_ping(): [ERROR] Server mysql-master:3306 missed 3 heartbeats, shunning it and killing all the connections. Disabling other checks until the node comes back online.
```
### Get status from ProxySQL
```aiignore
docker exec -it proxysql mysql -u admin -padmin -h 127.0.0.1 -P 6032 -e "SELECT hostgroup, srv_host, srv_port, status FROM stats_mysql_connection_pool;"
+-----------+----------------+----------+---------+
| hostgroup | srv_host       | srv_port | status  |
+-----------+----------------+----------+---------+
| 10        | mysql-master   | 3306     | SHUNNED |
| 20        | mysql-replica1 | 3306     | ONLINE  |
| 20        | mysql-replica2 | 3306     | ONLINE  |
+-----------+----------------+----------+---------+
```
### Write fails after master is down
```aiignore
db_proxy_mysql % python app.py 
--- Connected to ProxySQL ---

[Write] Writing new character...
Error: 9001 (HY000): Max connect timeout reached while reaching hostgroup 10 after 10004ms
```
### Accepting writes on Replica1
```aiignore
(.venv)db_proxy_mysql % sh build/allow_writes_on_replica1.sh                                                                  
mysql: [Warning] Using a password on the command line interface can be insecure.
+-----------+----------------+----------+--------------+----------+----------+--------+---------+-------------+---------+-------------------+-----------------+-----------------+------------+
| hostgroup | srv_host       | srv_port | status       | ConnUsed | ConnFree | ConnOK | ConnERR | MaxConnUsed | Queries | Queries_GTID_sync | Bytes_data_sent | Bytes_data_recv | Latency_us |
+-----------+----------------+----------+--------------+----------+----------+--------+---------+-------------+---------+-------------------+-----------------+-----------------+------------+
| 10        | mysql-master   | 3306     | ONLINE       | 0        | 0        | 1      | 16      | 1           | 2       | 0                 | 102             | 0               | 228        |
| 10        | mysql-replica1 | 3306     | ONLINE       | 0        | 0        | 0      | 0       | 0           | 0       | 0                 | 0               | 0               | 0          |
| 20        | mysql-replica1 | 3306     | OFFLINE_HARD | 0        | 0        | 0      | 0       | 0           | 0       | 0                 | 0               | 0               | 299        |
| 20        | mysql-replica2 | 3306     | ONLINE       | 0        | 1        | 1      | 0       | 1           | 1       | 0                 | 71              | 17              | 326        |
+-----------+----------------+----------+--------------+----------+----------+--------+---------+-------------+---------+-------------------+-----------------+-----------------+------------+
(.venv)db_proxy_mysql % python app.py                                                                                         
--- Connected to ProxySQL ---

[Write] Writing new character...
Write successful!

[Read] Fetching data...
Data received from Server ID: 3
Name: Sathya Raj
```
However, since replica2 is still trying to get replication from master, 
replication will not be happening unless we update replication source to replica1
