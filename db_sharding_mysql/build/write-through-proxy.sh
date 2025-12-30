docker exec proxysql mysql -uroot -proot123 -h 127.0.0.1 -P 6033 -e "INSERT INTO sharding_db.Users (fname, lname) VALUES ('Arun', 'Saxena');"
docker exec proxysql mysql -uroot -proot123 -h 127.0.0.1 -P 6033 -e "INSERT INTO sharding_db.Users (fname, lname) VALUES ('Krishna', 'Das');"
docker exec proxysql mysql -uroot -proot123 -h 127.0.0.1 -P 6033 -e "INSERT INTO sharding_db.Users (fname, lname) VALUES ('Tarun', 'Shah');"
