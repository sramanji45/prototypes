### Start mysql shard servers
```
cd db_sharding_mysql/build
$docker compose --verbose up -d
DEBU[0000] local image mysql:8.0.35 doesn't match expected platform linux/amd64 
[+] Running 3/3
 ✔ mysql-shard2 Pulled                                                                                                                                          2.3s 
 ✔ mysql-shard3 Pulled                                                                                                                                          2.3s 
 ✔ mysql-shard1 Pulled                                                                                                                                          2.3s 
[+] Running 0/1
 ⠋ Network build_mysql-network  Creating                                                                                                                        0.0s 
[+] Running 5/5d orphan containers ([build-user-service-1]) for this project. If you removed or renamed this service in your compose file, you can run this command w ✔ Network build_mysql-network  Created                                                                                                                         0.0s 
 ✔ Container proxysql           Started                                                                                                                         0.2s 
 ✔ Container shard1-master      Started                                                                                                                         0.2s 
 ✔ Container shard2-master      Started                                                                                                                         0.2s 
 ✔ Container shard3-master      Started                                                                                                                       0.2s 
```
### Ensure all services are running
```
$docker ps
CONTAINER ID   IMAGE                      COMMAND                  CREATED          STATUS          PORTS                                                             NAMES
f31055a8c379   mysql:8.0.35               "docker-entrypoint.s…"   32 seconds ago   Up 32 seconds   0.0.0.0:33063->3306/tcp, [::]:33063->3306/tcp                     shard3-master
8adbb351b5de   mysql:8.0.35               "docker-entrypoint.s…"   32 seconds ago   Up 32 seconds   0.0.0.0:33062->3306/tcp, [::]:33062->3306/tcp                     shard2-master
e276a84ffb2b   proxysql/proxysql:latest   "proxysql -f --idle-…"   32 seconds ago   Up 32 seconds   0.0.0.0:6032-6033->6032-6033/tcp, [::]:6032-6033->6032-6033/tcp   proxysql
99e369191558   mysql:8.0.35               "docker-entrypoint.s…"   32 seconds ago   Up 32 seconds   0.0.0.0:33061->3306/tcp, [::]:33061->3306/tcp                     shard1-master
```
### Setup Replicas
```aiignore
$sh setup-replicas.sh 
mysql: [Warning] Using a password on the command line interface can be insecure.
mysql: [Warning] Using a password on the command line interface can be insecure.
mysql: [Warning] Using a password on the command line interface can be insecure.
mysql: [Warning] Using a password on the command line interface can be insecure.
mysql: [Warning] Using a password on the command line interface can be insecure.
mysql: [Warning] Using a password on the command line interface can be insecure.
```
### Ensure replicas are running fine
```aiignore
shard3-master  | 2025-12-30T13:17:54.846385Z 9 [System] [MY-014001] [Repl] Replica receiver thread for channel '': connected to source 'replica_user@mysql-shard2:3306' with server_uuid=64b43b64-e581-11f0-b837-924f93b36477, server_id=2. Starting replication from file 'mysql-bin.000003', position '157'
shard2-master  | 2025-12-30T13:17:54.633834Z 9 [System] [MY-014001] [Repl] Replica receiver thread for channel '': connected to source 'replica_user@mysql-shard1:3306' with server_uuid=64a87bc8-e581-11f0-b837-4256bbd4745c, server_id=1. Starting replication from file 'mysql-bin.000003', position '157'.
shard1-master  | 2025-12-30T13:17:55.030451Z 11 [System] [MY-014001] [Repl] Replica receiver thread for channel '': connected to source 'replica_user@mysql-shard3:3306' with server_uuid=64b9e2ad-e581-11f0-b843-0eb3ec72e1af, server_id=3. Starting replication from file 'mysql-bin.000003', position '157'.
```

### Create Database and Tables 
```aiignore
docker exec -i shard1-master mysql -uroot -proot123 < create-database.sql
```
#### Get Databases from other shards and see if replication is working fine or not
```aiignore
$docker exec shard3-master mysql -uroot -proot123 -e "SHOW DATABASES;"
mysql: [Warning] Using a password on the command line interface can be insecure.
Database
information_schema
mysql
performance_schema
sharding_db
sys
--------------------------------------------------------------------------------------------
$docker exec shard2-master mysql -uroot -proot123 -e "SHOW DATABASES;"
mysql: [Warning] Using a password on the command line interface can be insecure.
Database
information_schema
mysql
performance_schema
sharding_db
sys
```
### Write data through ProxySQL
```aiignore
$sh write-through-proxy.sh
```
### Verify ProxySQL routing
```aiignore
$sh verify-proxysql.sh 
srv_host	Queries
mysql-shard1	1
mysql-shard2	1
mysql-shard3	1
```
### Test different scenarios
```aiignore
$docker exec proxysql mysql -uroot -proot123 -h 127.0.0.1 -P 6033 -e "INSERT INTO sharding_db.Users (fname, lname) VALUES ('Badri', 'Nadh');"  
$sh verify-proxysql.sh
srv_host	Queries
mysql-shard1	2
mysql-shard2	1
mysql-shard3	1
```

