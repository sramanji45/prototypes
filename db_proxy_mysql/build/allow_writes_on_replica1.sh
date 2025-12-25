docker exec -it mysql-replica1 mysql -uroot -proot123 -e "SET GLOBAL read_only = 0;"

docker exec -it proxysql mysql -u admin -padmin -h 127.0.0.1 -P 6032 -e "
/* 1. Move replica1 to the Writer group */
UPDATE mysql_servers SET hostgroup_id=10 WHERE hostname='mysql-replica1';

/* 2. Load the changes into memory */
LOAD MYSQL SERVERS TO RUNTIME;

/* 3. Make it permanent (saves to the internal SQLite db) */
SAVE MYSQL SERVERS TO DISK;
"

docker exec -it proxysql mysql -u admin -padmin -h 127.0.0.1 -P 6032 -e "SELECT * FROM stats.stats_mysql_connection_pool;"