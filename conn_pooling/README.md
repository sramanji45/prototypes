docker pull mysql

docker run --name my-mysql \
  -e MYSQL_ROOT_PASSWORD=root123 \
  -e MYSQL_USER=mysql \
  -e MYSQL_PASSWORD=mysql123 \
  -e MYSQL_DATABASE=conn_pooling \
  -p 3306:3306 -d mysql

docker exec -it my-mysql mysql -u mysql -p

username:password@tcp(address:port)/dbname

go get github.com/go-sql-driver/mysql

go run main.go