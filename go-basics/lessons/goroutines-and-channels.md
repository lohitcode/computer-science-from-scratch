# Goroutines & Channels - Complete Guide

**Go's superpower: Simple, safe concurrency**

---

## 📚 Table of Contents

1. [What & Why](#what--why)
2. [Goroutines Explained](#goroutines-explained)
3. [Channels Explained](#channels-explained)
4. [Production Use Cases](#production-use-cases)
5. [Where You'll Use This](#where-youll-use-this)
6. [Common Patterns](#common-patterns)
7. [Pitfalls to Avoid](#pitfalls-to-avoid)

---

## 🎯 What & Why

### The Problem: Blocking Code

```go
// Traditional (blocking) - SLOW!
func fetchUser() User {
    time.Sleep(2 * time.Second)  // Simulate DB call
    return User{Name: "Lohit"}
}

func fetchOrders() []Order {
    time.Sleep(2 * time.Second)  // Simulate API call
    return []Order{{ID: 1}}
}

func main() {
    start := time.Now()

    user := fetchUser()      // Waits 2 seconds
    orders := fetchOrders()  // Waits 2 seconds

    fmt.Println(user, orders)
    fmt.Printf("Total: %s\n", time.Since(start))  // 4 seconds!
}
```

**Problem:** Each function blocks the next. Total time = sum of all delays.

---

### The Solution: Goroutines (Non-blocking!)

```go
func main() {
    start := time.Now()

    // Start both concurrently!
    go func() {
        user = fetchUser()
    }()

    go func() {
        orders = fetchOrders()
    }()

    // Wait for both to complete
    time.Sleep(2 * time.Second)

    fmt.Println(user, orders)
    fmt.Printf("Total: %s\n", time.Since(start))  // ~2 seconds!
}
```

**Result:** Both run at once! Total time ≈ max delay, not sum.

---

## 🧵 Goroutines Explained

### What is a Goroutine?

**Goroutine** = Lightweight thread managed by Go runtime

| Feature | OS Thread | Goroutine |
|---------|-----------|-----------|
| **Memory** | ~1MB stack | ~2KB stack |
| **Creation** | Slow (system call) | Instant |
| **Switching** | OS scheduler | Go scheduler |
| **Count** | Thousands | **Millions!** |

---

### Creating Goroutines

```go
// Regular function call (blocking)
doWork()

// Goroutine call (non-blocking)
go doWork()

// Anonymous function as goroutine
go func() {
    fmt.Println("Running in background!")
}()

// With parameters
go func(msg string) {
    fmt.Println(msg)
}("Hello from goroutine!")
```

---

### Real-World Example: Web Scraper

```go
func scrape(url string) string {
    time.Sleep(time.Second)  // Simulate network delay
    return fmt.Sprintf("Data from %s", url)
}

func main() {
    urls := []string{
        "https://api1.com",
        "https://api2.com",
        "https://api3.com",
    }

    // Sequential: 3 seconds
    for _, url := range urls {
        scrape(url)
    }

    // Concurrent: 1 second!
    for _, url := range urls {
        go scrape(url)
    }
}
```

---

## 📡 Channels Explained

### What is a Channel?

**Channel** = Pipe for communicating between goroutines

```
Goroutine A ──[channel]──> Goroutine B
     (send)                  (receive)
```

**Why channels?** Goroutines need to coordinate and share data safely!

---

### Creating & Using Channels

```go
// Create channel
ch := make(chan string)

// Send (blocks until someone receives)
ch <- "hello"

// Receive (blocks until someone sends)
msg := <-ch

// Receive and discard
<-ch
```

---

### Channel Example: Worker Pool

```go
func worker(id int, jobs <-chan int, results chan<- int) {
    for job := range jobs {
        fmt.Printf("Worker %d processing job %d\n", id, job)
        time.Sleep(time.Second)  // Simulate work
        results <- job * 2        // Send result
    }
}

func main() {
    jobs := make(chan int, 100)
    results := make(chan int, 100)

    // Start 3 workers
    for w := 1; w <= 3; w++ {
        go worker(w, jobs, results)
    }

    // Send 5 jobs
    for j := 1; j <= 5; j++ {
        jobs <- j
    }
    close(jobs)

    // Collect results
    for r := 1; r <= 5; r++ {
        <-results
    }
}
```

---

## 🏭 Production Use Cases

### 1. API Servers (FastAPI competitors)

**Problem:** Handle thousands of concurrent requests

```go
// Gin/Echo framework uses goroutines per request
func handleRequest(c *gin.Context) {
    // Each request runs in its own goroutine
    user := fetchUser(c.Param("id"))
    orders := fetchOrders(c.Param("id"))
    c.JSON(200, gin.H{"user": user, "orders": orders})
}
```

**In production:** Every HTTP request = one goroutine. That's how Go serves 100k+ requests/second!

---

### 2. Microservices Communication

**Problem:** Call multiple services without blocking

```go
func getUserData(userID string) Response {
    var (
        user    User
        profile Profile
        orders  []Order
    )

    // Fan-out: Call all services at once!
    go func() { user = userService.Get(userID) }()
    go func() { profile = profileService.Get(userID) }()
    go func() { orders = orderService.Get(userID) }()

    // Wait for all (using sync.WaitGroup or channels)
    time.Sleep(500 * time.Millisecond)

    return Response{user, profile, orders}
}
```

**In production:** Microservices call each other concurrently. Response time drops from 500ms to 100ms!

---

### 3. Background Jobs & Workers

**Problem:** Process tasks asynchronously

```go
type Job struct {
    ID   int
    Data string
}

func worker(jobs <-chan Job) {
    for job := range jobs {
        processJob(job)  // Email, image resize, etc.
    }
}

func main() {
    jobs := make(chan Job, 1000)

    // Start 10 workers
    for i := 0; i < 10; i++ {
        go worker(jobs)
    }

    // Enqueue jobs (non-blocking!)
    jobs <- Job{ID: 1, Data: "send_email"}
    jobs <- Job{ID: 2, Data: "resize_image"}
}
```

**In production:** Background job processors (like Sidekiq in Ruby, Celery in Python).

---

### 4. Real-Time Systems (WebSockets)

**Problem:** Handle thousands of simultaneous WebSocket connections

```go
func handleWS(conn *websocket.Conn) {
    messages := make(chan string)

    // Read from client (goroutine 1)
    go func() {
        for {
            msg := readMessage(conn)
            messages <- msg
        }
    }()

    // Write to client (goroutine 2)
    go func() {
        for msg := range messages {
            conn.WriteMessage(msg)
        }
    }()
}
```

**In production:** Chat apps, live dashboards, collaborative editing.

---

### 5. Database Connection Pools

**Problem:** Share limited DB connections efficiently

```go
type Pool struct {
    connChan chan *sql.DB
}

func (p *Pool) Get() *sql.DB {
    return <-p.connChan  // Blocks until connection available
}

func (p *Pool) Put(conn *sql.DB) {
    p.connChan <- conn  // Return connection to pool
}

// Usage: Many goroutines share limited connections
go queryDatabase(pool)
go queryDatabase(pool)
go queryDatabase(pool)
```

---

### 6. Rate Limiting

**Problem:** Don't overwhelm external APIs

```go
// Allow 1 request per second
ticker := time.NewTicker(time.Second)
go func() {
    for range ticker.C {
        <-requestQueue  // Process one request
    }
}()
```

---

## 🎯 Where You'll Use This

### For Your Job Goals

| Scenario | How You'll Use It |
|----------|-------------------|
| **FastAPI → Gin** | Every request = goroutine |
| **RAG Systems** | Query vector DB + LLM concurrently |
| **API Integrations** | Call multiple 3rd-party APIs at once |
| **Background Jobs** | Email, webhooks, file processing |
| **Real-time Features** | WebSockets, live updates |

---

### Concrete Example: RAG System

```go
func ragQuery(query string) Response {
    var (
        embeddings []float32
        docs       []Document
        answer     string
    )

    // Step 1: Get embeddings (call OpenAI)
    go func() {
        embeddings = getEmbeddings(query)
    }()

    // Step 2: Search vector DB
    go func() {
        docs = searchVectorDB(query)
    }()

    // Wait for both
    time.Sleep(500 * time.Millisecond)

    // Step 3: Generate answer
    answer = generateAnswer(query, docs)

    return Response{Answer: answer, Sources: docs}
}
```

**Without goroutines:** 3 sequential calls = 3 seconds
**With goroutines:** 2 concurrent calls + 1 dependent = ~1.5 seconds

---

## 🔧 Common Patterns

### Pattern 1: Fan-Out (Parallel Processing)

```go
func processItems(items []Item) []Result {
    results := make(chan Result, len(items))

    // Start processing all items concurrently
    for _, item := range items {
        go func(i Item) {
            results <- processItem(i)
        }(item)
    }

    // Collect results
    var output []Result
    for range items {
        output = append(output, <-results)
    }
    return output
}
```

---

### Pattern 2: Fan-In (Aggregation)

```go
func merge(channels ...<-chan int) <-chan int {
    out := make(chan int)

    for _, ch := range channels {
        go func(c <-chan int) {
            for val := range c {
                out <- val
            }
        }(ch)
    }
    return out
}
```

---

### Pattern 3: Timeout Pattern

```go
func withTimeout[T any](fn func() T, timeout time.Duration) (T, error) {
    result := make(chan T, 1)

    go func() {
        result <- fn()
    }()

    select {
    case r := <-result:
        return r, nil
    case <-time.After(timeout):
        var zero T
        return zero, errors.New("timeout")
    }
}
```

---

### Pattern 4: Pipeline Processing

```go
// Stage 1: Generate
func generate(nums ...int) <-chan int {
    out := make(chan int)
    go func() {
        for _, n := range nums {
            out <- n
        }
        close(out)
    }()
    return out
}

// Stage 2: Double
func double(in <-chan int) <-chan int {
    out := make(chan int)
    go func() {
        for n := range in {
            out <- n * 2
        }
        close(out)
    }()
    return out
}

// Usage: Pipeline
c := generate(1, 2, 3, 4)
c = double(c)
for n := range c {
    fmt.Println(n)  // 2, 4, 6, 8
}
```

---

## ⚠️ Pitfalls to Avoid

### 1. Goroutine Leaks

```go
// BAD: Goroutine never exits
go func() {
    for {
        fmt.Println("Running forever!")
    }
}()

// GOOD: Use done channel
done := make(chan bool)
go func() {
    for {
        select {
        case <-done:
            return  // Exit cleanly
        default:
            fmt.Println("Working...")
        }
    }
}()
close(done)  // Signal goroutine to stop
```

---

### 2. Race Conditions

```go
// BAD: Data race!
var counter int
for i := 0; i < 1000; i++ {
    go func() {
        counter++  // Multiple goroutines writing same variable!
    }()
}

// GOOD: Use mutex
var mu sync.Mutex
var counter int
for i := 0; i < 1000; i++ {
    go func() {
        mu.Lock()
        counter++
        mu.Unlock()
    }()
}
```

---

### 3. Blocking on Unbuffered Channel

```go
// BAD: Deadlock!
ch := make(chan int)
ch <- 42  // Blocks forever! No receiver running

// GOOD: Buffered channel or start receiver first
ch := make(chan int, 1)
ch <- 42  // OK! Has buffer space
```

---

### 4. Forgetting to Close Channels

```go
// BAD: Receiver never knows channel is done
ch := make(chan int)
go func() {
    for i := range ch {  // Waits forever!
        fmt.Println(i)
    }
}()

// GOOD: Always close when done sending
close(ch)
```

---

## 📊 Performance Comparison

| Operation | Sequential | Concurrent | Speedup |
|-----------|-----------|------------|---------|
| 5 API calls (100ms each) | 500ms | 100ms | **5x** |
| Process 1000 items (10ms each) | 10s | ~50ms | **200x** |
| 3 DB queries (50ms each) | 150ms | 50ms | **3x** |

**Rule of thumb:** Any I/O operation is faster with goroutines!

---

## ✅ Summary

| Concept | Purpose | When to Use |
|---------|---------|-------------|
| **Goroutine** | Run code concurrently | I/O, background tasks |
| **Channel** | Communicate safely | Sharing data between goroutines |
| **Select** | Wait on multiple ops | Timeouts, multiple channels |
| **Mutex** | Protect shared data | When multiple goroutines write same variable |

---

## 🚀 Next Steps

1. Practice with the current problem
2. Build a concurrent web scraper
3. Try building a simple worker pool
4. Explore `sync.WaitGroup` for coordination

**This is Go's killer feature - master it and you'll write faster, more scalable services!**
