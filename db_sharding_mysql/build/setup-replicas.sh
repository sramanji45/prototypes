# 1. Shard 2 follows Shard 1
MS1_STATUS=$(docker exec shard1-master mysql -uroot -proot123 -e "SHOW MASTER STATUS\G")
FILE1=$(echo "$MS1_STATUS" | grep File | awk '{print $2}')
POS1=$(echo "$MS1_STATUS" | grep Position | awk '{print $2}')

docker exec shard2-master mysql -uroot -proot123 -e "STOP REPLICA; CHANGE REPLICATION SOURCE TO SOURCE_HOST='mysql-shard1', SOURCE_USER='replica_user', SOURCE_PASSWORD='password123', GET_SOURCE_PUBLIC_KEY=1, SOURCE_LOG_FILE='$FILE1', SOURCE_LOG_POS=$POS1; START REPLICA;"

# 2. Shard 3 follows Shard 2
MS2_STATUS=$(docker exec shard2-master mysql -uroot -proot123 -e "SHOW MASTER STATUS\G")
FILE2=$(echo "$MS2_STATUS" | grep File | awk '{print $2}')
POS2=$(echo "$MS2_STATUS" | grep Position | awk '{print $2}')

docker exec shard3-master mysql -uroot -proot123 -e "STOP REPLICA; CHANGE REPLICATION SOURCE TO SOURCE_HOST='mysql-shard2', SOURCE_USER='replica_user', SOURCE_PASSWORD='password123', GET_SOURCE_PUBLIC_KEY=1, SOURCE_LOG_FILE='$FILE2', SOURCE_LOG_POS=$POS2; START REPLICA;"

# 3. Shard 1 follows Shard 3
MS3_STATUS=$(docker exec shard3-master mysql -uroot -proot123 -e "SHOW MASTER STATUS\G")
FILE3=$(echo "$MS3_STATUS" | grep File | awk '{print $2}')
POS3=$(echo "$MS3_STATUS" | grep Position | awk '{print $2}')

docker exec shard1-master mysql -uroot -proot123 -e "STOP REPLICA; CHANGE REPLICATION SOURCE TO SOURCE_HOST='mysql-shard3', SOURCE_USER='replica_user', SOURCE_PASSWORD='password123', GET_SOURCE_PUBLIC_KEY=1, SOURCE_LOG_FILE='$FILE3', SOURCE_LOG_POS=$POS3; START REPLICA;"