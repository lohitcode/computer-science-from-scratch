# Goroutines & Channels - From Scratch to Mastery

**A complete story of concurrent programming in Go**

---

## 📖 Part 1: The Problem - Blocking Code

Let's start with WHY we need this.

### Story: The Coffee Shop (Sequential)

Imagine you own a coffee shop. You're the only employee.

```
Customer 1: "I want a latte" → You make it (2 mins)
Customer 2: "I want a cappuccino" → You make it (2 mins)
Customer 3: "I want an espresso" → You make it (2 mins)

Total time: 6 minutes
Customers 2 & 3 wait while you serve 1
```

This is **sequential/blocking code**:

```go
func makeCoffee(name string) {
    time.Sleep(2 * time.Second)  // Takes 2 minutes
    fmt.Printf("Here's your %s!\n", name)
}

func main() {
    start := time.Now()

    makeCoffee("latte")        // Blocks! Customer 2 waits
    makeCoffee("cappuccino")   // Blocks! Customer 3 waits
    makeCoffee("espresso")     // Finally served

    fmt.Printf("Total: %s\n", time.Since(start))  // 6 seconds
}
```

**Problem:** Each customer waits for the previous one!

---

### The Solution: Hire More Staff (Parallel)

Now imagine you have 3 employees:

```
Employee 1: Makes latte (2 mins)
Employee 2: Makes cappuccino (2 mins)  ┐
Employee 3: Makes espresso (2 mins)    ├→ All at once!

Total time: 2 minutes (not 6!)
```

This is **concurrent code** with **goroutines**!

---

## 🧵 Part 2: Goroutines - The Employees

### What is a Goroutine?

**Goroutine** = A function running independently (like an employee)

```go
// Regular function call (you doing everything yourself)
makeCoffee("latte")

// Goroutine (hiring an employee to do it)
go makeCoffee("latte")
```

The `go` keyword = "Hire someone to do this!"

---

### Your First Goroutine

```go
package main

import (
    "fmt"
    "time"
)

func makeCoffee(name string) {
    fmt.Printf("Started making %s...\n", name)
    time.Sleep(2 * time.Second)
    fmt.Printf("Finished %s!\n", name)
}

func main() {
    fmt.Println("Coffee shop opening!")

    // Hire 3 employees, all start at once!
    go makeCoffee("latte")
    go makeCoffee("cappuccino")
    go makeCoffee("espresso")

    // Main goroutine needs to wait!
    time.Sleep(3 * time.Second)

    fmt.Println("Coffee shop closing!")
}
```

**Output:**
```
Coffee shop opening!
Started making latte...
Started making cappuccino...
Started making espresso...
Finished latte!
Finished cappuccino!
Finished espresso!
Coffee shop closing!
Total: ~2 seconds (not 6!)
```

**Key insight:** All three coffees made at the same time!

---

### Why time.Sleep()?

You might wonder: Why do we need `time.Sleep()` at the end?

```go
go makeCoffee("latte")      // Employee starts working

// If main() exits here, the program ends immediately!
// The employee doesn't get to finish!

time.Sleep(3 * time.Second)  // Wait for employees to finish
```

**Think of it this way:**
- `main()` = The shop owner
- Goroutines = Employees
- If owner leaves, shop closes, employees sent home!

**We'll learn better ways to wait later (channels, WaitGroup).**

---

## 🔗 Part 3: The Communication Problem

### Story: Employees Need to Talk

Now imagine your coffee shop:

```
Employee 1 makes coffee → Needs to give it to Customer
Employee 2 makes coffee → Needs to give it to Customer
Employee 3 makes coffee → Needs to give it to Customer
```

**Problem:** How do employees give results back to the main program?

**Answer:** **Channels!**

---

## 📡 Part 4: Channels - The Conveyor Belt

### What is a Channel?

**Channel** = A conveyor belt for passing data between goroutines

```
┌─────────────┐         ┌─────────────┐
│  Goroutine  │ ──nail──>│   Channel   │<──mail─── │  Goroutine  │
│   (maker)   │         │ (conveyor)  │           │   (taker)   │
└─────────────┘         └─────────────┘           └─────────────┘
```

**Key concepts:**
1. **Send:** Put item on conveyor belt (`ch <- item`)
2. **Receive:** Take item from conveyor belt (`item := <-ch`)
3. **Block:** Wait if belt is full (send) or empty (receive)

---

### Your First Channel

```go
package main

import "fmt"

func main() {
    // Create a channel (like installing a conveyor belt)
    messages := make(chan string)

    // Hire an employee to make coffee
    go func() {
        fmt.Println("Employee: Making latte...")
        time.Sleep(2 * time.Second)
        fmt.Println("Employee: Done! Sending to channel...")

        // Send result to channel
        messages <- "Hot latte!"
    }()

    fmt.Println("Owner: Waiting for coffee...")

    // Receive from channel (blocks until available)
    msg := <-messages
    fmt.Printf("Owner: Received %s\n", msg)

    fmt.Println("Owner: Serving customer!")
}
```

**Output:**
```
Owner: Waiting for coffee...
Employee: Making latte...
Employee: Done! Sending to channel...
Owner: Received Hot latte!
Owner: Serving customer!
```

**What happened:**
1. Owner creates channel (conveyor belt)
2. Hires employee (goroutine)
3. Employee works in background
4. Owner waits at channel (`<-messages`)
5. Employee sends result (`messages <- "..."`)
6. Owner receives and serves

---

### Why Channels Block

**This is the magic!**

```go
messages := make(chan string)

// Send operation BLOCKS until someone receives
messages <- "hello"  // Waits forever if no one receives!

// Receive operation BLOCKS until someone sends
msg := <-messages    // Waits forever if no one sends!
```

**Why this is good:**
```go
go func() {
    messages <- "result"  // Waits here until main() is ready
}()

// Do other work...
time.Sleep(1 * time.Second)

// Now receive
result := <-messages  // Data is already there, no wait!
```

**Channels naturally coordinate goroutines!**

---

## 🎯 Part 5: Buffered vs Unbuffered Channels

### Unbuffered Channel (default)

```go
ch := make(chan int)  // Zero capacity
```

**Like a handshake:** Both parties must be present!

```
Sender: "I have something for you"
Receiver: "I'm ready"
Sender: "Here you go" ← Only now does send complete
```

**Example:**
```go
ch := make(chan string)

go func() {
    ch <- "ping"  // Blocks until someone receives
}()

fmt.Println(<-ch)  // Receives, now send completes
```

---

### Buffered Channel

```go
ch := make(chan int, 10)  // Can hold 10 items
```

**Like a mailbox:** Can drop items off, receiver checks later.

```
Sender: Drops letter in mailbox → Walks away
Receiver: Checks mailbox whenever
```

**Example:**
```go
ch := make(chan string, 2)  // Holds 2 items

ch <- "item1"  // Doesn't block!
ch <- "item2"  // Doesn't block!
// ch <- "item3"  // Would block! Mailbox full

<-ch  // Take one out
ch <- "item3"  // Now there's space!
```

---

## 🏭 Part 6: Worker Pools - Production Pattern

### The Pattern

**Problem:** Process 100 tasks, but only have 5 CPUs

**Solution:** Worker pool with 5 goroutines, task queue via channel

```go
package main

import (
    "fmt"
    "time"
)

// Worker: Represents an employee
func worker(id int, jobs <-chan int, results chan<- int) {
    for job := range jobs {
        fmt.Printf("Worker %d: Processing job %d\n", id, job)
        time.Sleep(time.Second)  // Simulate work
        results <- job * 2       // Send result
    }
    fmt.Printf("Worker %d: Done!\n", id)
}

func main() {
    // Create channels
    jobs := make(chan int, 100)    // Task queue
    results := make(chan int, 100)  // Results

    // Hire 3 workers (employees)
    for w := 1; w <= 3; w++ {
        go worker(w, jobs, results)
    }

    // Send 5 jobs (tasks)
    for j := 1; j <= 5; j++ {
        jobs <- j
    }
    close(jobs)  // No more jobs!

    // Collect results
    for r := 1; r <= 5; r++ {
        <-results
    }

    fmt.Println("All jobs done!")
}
```

**Output:**
```
Worker 1: Processing job 1
Worker 2: Processing job 2
Worker 3: Processing job 3
Worker 1: Processing job 4
Worker 2: Processing job 5
Worker 3: Done!
...
All jobs done!
```

**What happened:**
1. Created 3 workers (goroutines)
2. Sent 5 jobs to `jobs` channel
3. Each worker grabbed jobs from the channel
4. Workers sent results to `results` channel
5. Main collected results

**Time taken:** ~2 seconds (not 5!) because 3 workers in parallel!

---

## 🔀 Part 7: Select - Waiting on Multiple Channels

### The Problem

You're waiting for:
1. Coffee to be ready
2. Toast to pop
3. Whichever finishes first, you take it!

**Solution:** `select` statement

---

### Select Example

```go
package main

import (
    "fmt"
    "time"
)

func main() {
    coffee := make(chan string)
    toast := make(chan string)

    // Making coffee (slow)
    go func() {
        time.Sleep(2 * time.Second)
        coffee <- "Coffee ready!"
    }()

    // Making toast (fast)
    go func() {
        time.Sleep(1 * time.Second)
        toast <- "Toast popped!"
    }()

    // Wait for whichever finishes first
    select {
    case msg := <-coffee:
        fmt.Println("Got:", msg)
    case msg := <-toast:
        fmt.Println("Got:", msg)  // This wins!
    }

    fmt.Println("Breakfast served!")
}
```

**Output:**
```
Got: Toast popped!
Breakfast served!
```

**What happened:**
1. Both coffee and toast started
2. `select` waited for either
3. Toast finished first (1 second vs 2)
4. `select` took toast channel
5. Coffee result is discarded (goroutine exits)

---

## 🚦 Part 8: Sync Patterns - WaitGroup

### The Problem with time.Sleep()

Remember this?

```go
go makeCoffee("latte")
go makeCoffee("espresso")

time.Sleep(3 * time.Second)  // ⚠️ Guessing wait time!
```

**Problems:**
1. What if it takes 4 seconds? Race condition!
2. What if it takes 1 second? Wasted time!

**Solution:** `sync.WaitGroup`

---

### WaitGroup Example

```go
package main

import (
    "fmt"
    "sync"
    "time"
)

func makeCoffee(name string, wg *sync.WaitGroup) {
    defer wg.Done()  // "I'm done!" when function returns

    fmt.Printf("Making %s...\n", name)
    time.Sleep(2 * time.Second)
    fmt.Printf("%s ready!\n", name)
}

func main() {
    var wg sync.WaitGroup

    for _, drink := range []string{"latte", "cappuccino", "espresso"} {
        wg.Add(1)  // "One more task to wait for"
        go makeCoffee(drink, &wg)
    }

    wg.Wait()  // Wait for all tasks to call Done()
    fmt.Println("All drinks served!")
}
```

**Output:**
```
Making latte...
Making cappuccino...
Making espresso...
latte ready!
cappuccino ready!
espresso ready!
All drinks served!
```

**No guessing!** WaitGroup knows when all goroutines finish.

---

## ⚠️ Part 9: Common Pitfalls

### Pitfall 1: Goroutine Leak

```go
// BAD: Goroutine runs forever
go func() {
    for {
        fmt.Println("Leaking memory...")
    }
}()
```

**Fix:** Use done channel
```go
done := make(chan bool)
go func() {
    for {
        select {
        case <-done:
            return  // Exit cleanly
        default:
            fmt.Println("Working...")
            time.Sleep(time.Second)
        }
    }
}()
close(done)  // Signal to stop
```

---

### Pitfall 2: Race Condition

```go
// BAD: Two goroutines writing same variable
var counter int
go func() { counter++ }()
go func() { counter++ }()
// Both read, both write 1, result = 1 (should be 2!)
```

**Fix:** Mutex
```go
var mu sync.Mutex
var counter int

go func() {
    mu.Lock()
    counter++
    mu.Unlock()
}()
```

---

### Pitfall 3: Deadlock

```go
// BAD: Sending with no receiver
ch := make(chan int)
ch <- 42  // Blocks forever! No one receiving
```

**Fix:** Buffered channel or start receiver first
```go
ch := make(chan int, 1)
ch <- 42  // OK!
```

---

## 🎯 Part 10: Real-World Example

### Web Scraper - Sequential vs Concurrent

**Sequential (slow):**
```go
func scrape(urls []string) []string {
    var results []string
    for _, url := range urls {
        resp := fetch(url)  // Blocks!
        results = append(results, resp)
    }
    return results
}
// 10 URLs × 1 second each = 10 seconds
```

**Concurrent (fast):**
```go
func scrape(urls []string) []string {
    results := make(chan string, len(urls))

    // Start all fetches at once
    for _, url := range urls {
        go func(u string) {
            results <- fetch(u)
        }(url)
    }

    // Collect results
    var output []string
    for range urls {
        output = append(output, <-results)
    }
    return output
}
// 10 URLs in parallel = ~1 second!
```

---

## ✅ Summary: The Mental Model

### Goroutines = Employees
- Hire them with `go`
- They work independently
- Need coordination

### Channels = Communication
- Pass data safely
- Block until both parties ready
- Coordinate naturally

### Patterns
- **Worker pool:** Fixed workers, task queue
- **Fan-out:** Start many goroutines
- **Fan-in:** Collect results into one channel
- **Select:** Wait for multiple channels
- **WaitGroup:** Wait for all to finish

---

## 🚀 Next Steps

1. Try the current problem (Problem 12)
2. Build a concurrent web scraper
3. Implement a worker pool
4. Practice with different patterns

**This is Go's killer feature - you now understand it from first principles!**
