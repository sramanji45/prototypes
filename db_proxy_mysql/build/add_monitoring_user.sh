docker exec mysql-replica1 mysql -uroot -proot123 -e "CREATE USER IF NOT EXISTS 'replica_user'@'%' IDENTIFIED WITH mysql_native_password BY 'password123';GRANT ALL PRIVILEGES ON *.* TO 'replica_user'@'%';FLUSH PRIVILEGES;"
docker exec mysql-replica2 mysql -uroot -proot123 -e "CREATE USER IF NOT EXISTS 'replica_user'@'%' IDENTIFIED WITH mysql_native_password BY 'password123';GRANT ALL PRIVILEGES ON *.* TO 'replica_user'@'%';FLUSH PRIVILEGES;"

