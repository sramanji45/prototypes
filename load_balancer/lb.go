package main

import (
	"fmt"
	"io"
	"log"
	"net"
	"sync"
	"sync/atomic"

	"github.com/google/uuid"
)

type Backend struct {
	Host        string
	Port        int
	IsHealthy   bool
	NumRequests int64 // Changed to int64 for atomic operations
}

func (b *Backend) String() string {
	return fmt.Sprintf("%s:%d", b.Host, b.Port)
}

type LB struct {
	backends []*Backend
	mu       sync.RWMutex // Protects the backends slice
	current  uint64       // For Round Robin
}

type IncomingReq struct {
	srcConn net.Conn
	reqId   string
}

// GetNextBackend now uses Round Robin and is Thread-Safe
func (lb *LB) GetNextBackend() *Backend {
	lb.mu.RLock()
	defer lb.mu.RUnlock()

	// Atomic increment to avoid race conditions on the counter
	next := atomic.AddUint64(&lb.current, 1)
	idx := next % uint64(len(lb.backends))
	return lb.backends[idx]
}

func (lb *LB) Proxy(req IncomingReq) {
	defer req.srcConn.Close() // Ensure client connection closes

	backend := lb.GetNextBackend()
	log.Printf("[ID:%s] Routing to -> %s", req.reqId, backend.String())

	backendConn, err := net.Dial("tcp", backend.String())
	if err != nil {
		log.Printf("Backend %s unreachable: %v", backend.String(), err)
		return
	}
	defer backendConn.Close() // Ensure backend connection closes

	// Safely increment request count
	atomic.AddInt64(&backend.NumRequests, 1)

	// Bi-directional copy
	var wg sync.WaitGroup
	wg.Add(2)
	go func() {
		io.Copy(backendConn, req.srcConn)
		wg.Done()
	}()
	go func() {
		io.Copy(req.srcConn, backendConn)
		wg.Done()
	}()
	wg.Wait() // Wait for both streams to finish
}

func main() {
	// 1. Initialize Backends
	lb := &LB{
		backends: []*Backend{
			{Host: "localhost", Port: 8001, IsHealthy: true},
			{Host: "localhost", Port: 8002, IsHealthy: true},
			{Host: "localhost", Port: 8003, IsHealthy: true},
		},
	}

	// 2. Start Listener
	listener, err := net.Listen("tcp", ":9090")
	if err != nil {
		log.Fatal(err)
	}
	log.Println("Load Balancer active on :9090")

	for {
		conn, err := listener.Accept()
		if err != nil {
			log.Printf("Accept error: %v", err)
			continue // Don't panic! Just keep going.
		}

		go lb.Proxy(IncomingReq{
			srcConn: conn,
			reqId:   uuid.NewString()[:8], // Short ID for logs
		})
	}
}
