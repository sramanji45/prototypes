# Deploy MySQL master and replicas using docker-compose
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
## Debugging Help ##
#### Check Docker Compose logs
```
docker compose logs -f 
```
#### Log into MySQL and run SQL Commands
```
(.venv) ####@####-MacBook-Pro build % docker exec -it mysql-master bash
bash-4.4# mysql -u root -p
Enter password: 
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 8
Server version: 8.0.35 MySQL Community Server - GPL

Copyright (c) 2000, 2023, Oracle and/or its affiliates.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql> show databases;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| mysql              |
| performance_schema |
| sys                |
+--------------------+
5 rows in set (0.04 sec)

mysql> show master status;
+------------------+----------+--------------+------------------+-------------------+
| File             | Position | Binlog_Do_DB | Binlog_Ignore_DB | Executed_Gtid_Set |
+------------------+----------+--------------+------------------+-------------------+
| mysql-bin.000003 |      157 |              |                  |                   |
+------------------+----------+--------------+------------------+-------------------+
1 row in set (0.00 sec)

mysql> exit;
Bye
bash-4.4# exit
exit
```
### Check MySQL version
```
docker exec -it mysql-master mysql -V
mysql  Ver 8.0.35 for Linux on x86_64 (MySQL Community Server - GPL)
```
### Set up replicas
```
sh setup-replicas.sh
```
### Write to Master
```
docker exec -i mysql-master mysql -uroot -proot123 < write-to-master.sql
```
## READ FROM A REPLICA ##
```
(.venv) ####@####-MacBook-Pro build % docker exec -it mysql-replica1 bash
bash-4.4# mysql -u root -p
Enter password: 
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 22
Server version: 8.0.35 MySQL Community Server - GPL

Copyright (c) 2000, 2023, Oracle and/or its affiliates.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql> show databases;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| master_replicas_db |
| mysql              |
| performance_schema |
| sys                |
+--------------------+
5 rows in set (0.01 sec)

mysql> use master_replicas_db;
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A

Database changed
mysql> show tables;
+------------------------------+
| Tables_in_master_replicas_db |
+------------------------------+
| Bahubali                     |
+------------------------------+
1 row in set (0.01 sec)

mysql> select * from Bahubali;
+----+-----------+------------+---------------+-----------+
| id | fname     | lname      | role          | salary    |
+----+-----------+------------+---------------+-----------+
|  5 | Prabhas   | Raju       | Actor         |  50000.00 |
|  6 | Rana      | Dhaggubati | Actor         |  50000.00 |
|  7 | Rajamouli | SS         | Director      | 175000.00 |
|  8 | Keeravani | MM         | MusicDirector |  75000.00 |
+----+-----------+------------+---------------+-----------+
4 rows in set (0.00 sec)

mysql> exit
Bye
bash-4.4# exit
exit
```
### Replication Lag
```
(.venv) ####@####-MacBook-Pro build % docker exec mysql-replica1 mysql -uroot -proot123 -e "SHOW REPLICA STATUS\G" | grep "Seconds_Behind_Source"
mysql: [Warning] Using a password on the command line interface can be insecure.
        Seconds_Behind_Source: 0
```
