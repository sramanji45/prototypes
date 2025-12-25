# Get current log file and position from master
MS_STATUS=$(docker exec mysql-master mysql -uroot -proot123 -e "SHOW MASTER STATUS\G")
LOG_FILE=$(echo "$MS_STATUS" | grep File | awk '{print $2}')
LOG_POS=$(echo "$MS_STATUS" | grep Position | awk '{print $2}')

echo $LOG_FILE
echo $LOG_POS

# Feed them into the replicas
docker exec mysql-replica1 mysql -uroot -proot123 -e "STOP REPLICA; CHANGE REPLICATION SOURCE TO SOURCE_HOST='mysql-master', SOURCE_USER='replica_user', SOURCE_PASSWORD='password123', GET_SOURCE_PUBLIC_KEY=1, SOURCE_LOG_FILE='$LOG_FILE', SOURCE_LOG_POS=$LOG_POS; START REPLICA; SHOW REPLICA STATUS\G"
docker exec mysql-replica2 mysql -uroot -proot123 -e "STOP REPLICA; CHANGE REPLICATION SOURCE TO SOURCE_HOST='mysql-master', SOURCE_USER='replica_user', SOURCE_PASSWORD='password123', GET_SOURCE_PUBLIC_KEY=1, SOURCE_LOG_FILE='$LOG_FILE', SOURCE_LOG_POS=$LOG_POS; START REPLICA; SHOW REPLICA STATUS\G"