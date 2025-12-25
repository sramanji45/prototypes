CREATE USER 'replica_user'@'%' IDENTIFIED BY 'password123'; GRANT REPLICATION SLAVE ON *.* TO 'replica_user'@'%';

