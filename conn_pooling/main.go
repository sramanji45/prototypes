package main

import (
	"database/sql"
	"fmt"
	"sync"
	"time"

	_ "github.com/go-sql-driver/mysql"
)

type conn struct {
	db *sql.DB
}

type cpool struct {
	mu      *sync.Mutex
	channel chan interface{}
	conns   []*conn
	maxConn int
}

func NewConn() *sql.DB {
	user := "mysql"
	pass := "mysql123"
	host := "localhost"
	port := 3306
	dbname := "my_database"
	dsn := fmt.Sprintf("%s:%s@tcp(%s:%d)/%s?parseTime=true", user, pass, host, port, dbname)

	_db, err := sql.Open("mysql", dsn)
	if err != nil {
		panic(err)
	}
	return _db
}

func NewCPool(maxConn int) (*cpool, error) {
	var mu = sync.Mutex{}
	pool := &cpool{
		mu:      &mu,
		conns:   make([]*conn, 0, maxConn),
		channel: make(chan interface{}, maxConn),
		maxConn: maxConn,
	}
	for i := 0; i < maxConn; i++ {
		pool.conns = append(pool.conns, &conn{NewConn()})
		pool.channel <- nil
	}
	return pool, nil
}

func (pool *cpool) Get() (*conn, error) {
	<-pool.channel
	pool.mu.Lock()
	defer pool.mu.Unlock()

	lastIndex := len(pool.conns) - 1
	c := pool.conns[lastIndex]
	pool.conns = pool.conns[:lastIndex]

	return c, nil
}

func (pool *cpool) Put(c *conn) {
	pool.mu.Lock()
	defer pool.mu.Unlock()
	pool.conns = append(pool.conns, c)
	pool.channel <- nil
}

func (pool *cpool) Close() {
	close(pool.channel)
	for i := range pool.conns {
		pool.conns[i].db.Close()
	}
}

func BenchmarkNonPool() {
	startTime := time.Now()
	var wg sync.WaitGroup
	for i := 0; i < 50; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			conn := NewConn()
			_, err := conn.Exec("SELECT SLEEP(0.01);")
			if err != nil {
				panic(err)
			}
			conn.Close()
		}()
	}
	wg.Wait()
	fmt.Println("Benchmark Non Connection Pool", time.Since(startTime))
}

func BenchmarkPool() {
	startTime := time.Now()
	pool, err := NewCPool(10)
	if err != nil {
		panic(err)
	}
	var wg sync.WaitGroup
	for i := 0; i < 500; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			conn, err := pool.Get()
			if err != nil {
				panic(err)
			}
			_, err = conn.db.Exec("SELECT SLEEP(0.01);")
			if err != nil {
				panic(err)
			}
			pool.Put(conn)
		}()
	}
	fmt.Println("Benchmark with Connection Pool", time.Since(startTime))
}

func main() {
	//BenchmarkNonPool()
	BenchmarkPool()
}
