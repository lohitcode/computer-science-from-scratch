# WaitGroups in Go - Complete Guide

**The proper way to wait for goroutines**

---

## 🎯 The Problem: Goroutines Need Coordination

### Story: The Bus Leaving

Imagine you're a bus driver (main goroutine):

```
Driver: "Everyone get on!"
Passengers: (boarding goroutines)
Driver: "OK, I'm leaving!" ← Problem: Passengers still boarding!
```

Without coordination, the driver leaves before passengers finish!

---

## 📚 What is a WaitGroup?

**WaitGroup** = A counter that tracks how many goroutines are running

```go
import "sync"

var wg sync.WaitGroup
```

**Three operations:**
1. `wg.Add(n)` - "I expect n goroutines"
2. `wg.Done()` - "One goroutine finished" (decrements counter)
3. `wg.Wait()` - "Wait until counter is 0"

---

## 🔢 Visual: The Counter

```
┌─────────────────────────────────┐
│         WaitGroup Counter       │
├─────────────────────────────────┤
│  wg.Add(3)    → Counter = 3    │  "3 tasks to wait for"
│  wg.Done()    → Counter = 2    │  "2 tasks remaining"
│  wg.Done()    → Counter = 1    │  "1 task remaining"
│  wg.Done()    → Counter = 0    │  "All done! wg.Wait() returns"
└─────────────────────────────────┘
```

---

## 📖 Part 1: Basic Example

### Without WaitGroup (broken)

```go
func main() {
    for i := 0; i < 3; i++ {
        go func(n int) {
            fmt.Printf("Goroutine %d working...\n", n)
            time.Sleep(time.Second)
            fmt.Printf("Goroutine %d done!\n", n)
        }(i)
    }
    // Program exits immediately! Goroutines don't finish.
}
```

**Output:**
```
(maybe nothing, or partial output)
```

---

### With WaitGroup (correct)

```go
package main

import (
    "fmt"
    "sync"
    "time"
)

func worker(id int, wg *sync.WaitGroup) {
    defer wg.Done()  // "I'm done!" when function exits

    fmt.Printf("Worker %d starting...\n", id)
    time.Sleep(time.Second)
    fmt.Printf("Worker %d done!\n", id)
}

func main() {
    var wg sync.WaitGroup

    // Hire 3 workers
    for i := 1; i <= 3; i++ {
        wg.Add(1)  // "One more task to wait for"
        go worker(i, &wg)
    }

    wg.Wait()  // "Wait for all workers"
    fmt.Println("All workers finished!")
}
```

**Output:**
```
Worker 1 starting...
Worker 2 starting...
Worker 3 starting...
Worker 1 done!
Worker 2 done!
Worker 3 done!
All workers finished!
```

---

## 🔍 Part 2: How It Works

### Step by Step

```go
var wg sync.WaitGroup  // Counter starts at 0

wg.Add(3)              // Counter = 3
go func() {
    defer wg.Done()     // Will decrement when done
    // ... work ...
}()
go func() {
    defer wg.Done()     // Will decrement when done
    // ... work ...
}()
go func() {
    defer wg.Done()     // Will decrement when done
    // ... work ...
}()

wg.Wait()              // Blocks until counter = 0
```

**Timeline:**
```
0ms:   wg.Add(3) → Counter = 3
       [goroutine 1 starts]
       [goroutine 2 starts]
       [goroutine 3 starts]
       wg.Wait() blocks...

500ms: [still working...]
       Counter = 3

1000ms: goroutine 1 calls wg.Done() → Counter = 2
        goroutine 2 calls wg.Done() → Counter = 1
        goroutine 3 calls wg.Done() → Counter = 0

        wg.Wait() unblocks!
        "All workers finished!"
```

---

## 🎯 Part 3: defer wg.Done() Pattern

### Why use defer?

```go
// Without defer (easy to forget)
func worker(wg *sync.WaitGroup) {
    // ... lots of code ...
    if error {
        return  // Oops! Forgot wg.Done()
    }
    wg.Done()  // Never reached if error!
}

// With defer (always runs)
func worker(wg *sync.WaitGroup) {
    defer wg.Done()  // Guaranteed to run
    // ... lots of code ...
    if error {
        return  // defer wg.Done() still runs!
    }
}
```

**defer runs no matter how function exits:**
- Normal return
- Early return
- Panic (crash)

---

## 🔧 Part 4: Common Patterns

### Pattern 1: Fixed Number of Goroutines

```go
func main() {
    var wg sync.WaitGroup
    numWorkers := 5

    wg.Add(numWorkers)  // Add all at once
    for i := 0; i < numWorkers; i++ {
        go func(id int) {
            defer wg.Done()
            fmt.Printf("Worker %d\n", id)
        }(i)
    }

    wg.Wait()
}
```

---

### Pattern 2: Dynamic Goroutines

```go
func processItem(item int, wg *sync.WaitGroup) {
    defer wg.Done()
    // Process item...
}

func main() {
    items := []int{1, 2, 3, 4, 5}
    var wg sync.WaitGroup

    for _, item := range items {
        wg.Add(1)  // Add one per item
        go processItem(item, &wg)
    }

    wg.Wait()
}
```

---

### Pattern 3: Nested WaitGroups

```go
func main() {
    var outerWG sync.WaitGroup

    for i := 0; i < 3; i++ {
        outerWG.Add(1)
        go func(groupID int) {
            defer outerWG.Done()

            // Inner wait group
            var innerWG sync.WaitGroup
            for j := 0; j < 3; j++ {
                innerWG.Add(1)
                go func(taskID int) {
                    defer innerWG.Done()
                    fmt.Printf("Group %d, Task %d\n", groupID, taskID)
                }(taskID)
            }
            innerWG.Wait()  // Wait for inner tasks
        }(groupID)
    }

    outerWG.Wait()  // Wait for all groups
}
```

---

## ⚠️ Part 5: Common Mistakes

### Mistake 1: Forgetting to Add

```go
// BAD
wg.Add(1)
go func() {
    // defer wg.Done()  ← Oops! Forgot!
}()

wg.Wait()  // Blocks forever!
```

---

### Mistake 2: Wrong Add Count

```go
// BAD
wg.Add(3)  // Says "expecting 3"
go worker()
go worker()  // Only started 2!

wg.Wait()  // Blocks forever! Waiting for 3rd that never comes
```

---

### Mistake 3: Add After Goroutine Started

```go
// BAD
go func() {
    defer wg.Done()
    work()
}()
wg.Add(1)  // ← Race condition! Might add after goroutine finishes!

// CORRECT
wg.Add(1)
go func() {
    defer wg.Done()
    work()
}()
```

---

### Mistake 4: Passing by Value

```go
// BAD - wg is copied!
func worker(wg sync.WaitGroup) {  // ← No pointer!
    defer wg.Done()  // Modifies copy, not original!
}

// GOOD - wg is passed by reference
func worker(wg *sync.WaitGroup) {
    defer wg.Done()  // Modifies the original!
}
```

---

## 🏆 Part 6: Real-World Example

### Web Scraper with WaitGroup

```go
package main

import (
    "fmt"
    "sync"
    "time"
)

func scrape(url string, wg *sync.WaitGroup) {
    defer wg.Done()

    fmt.Printf("Scraping %s...\n", url)
    time.Sleep(time.Second)  // Simulate network delay
    fmt.Printf("Done: %s\n", url)
}

func main() {
    urls := []string{
        "https://example.com",
        "https://google.com",
        "https://github.com",
    }

    var wg sync.WaitGroup

    // Start all scrapers
    for _, url := range urls {
        wg.Add(1)
        go scrape(url, &wg)
    }

    // Wait for all to finish
    wg.Wait()
    fmt.Println("All scraping done!")
}
```

**Output:**
```
Scraping https://example.com...
Scraping https://google.com...
Scraping https://github.com...
Done: https://github.com
Done: https://example.com
Done: https://google.com
All scraping done!
```

**Time taken:** ~1 second (not 3!) because all run concurrently.

---

## 🎯 Part 7: WaitGroup vs Other Methods

### Comparison Table

| Method | Use Case | Pros | Cons |
|--------|----------|------|------|
| **WaitGroup** | Wait for N goroutines | Simple, no coordination | Can't return values |
| **Channels** | Pass data between goroutines | Can return values | More code |
| **time.Sleep** | Quick and dirty | Simple | Unreliable, wasteful |
| **Context** | Cancel goroutines | Can cancel/timeout | More complex |

---

### When to Use What

```go
// Use WaitGroup when: Just waiting for completion
var wg sync.WaitGroup
wg.Add(3)
go func() { defer wg.Done(); work() }()
go func() { defer wg.Done(); work() }()
go func() { defer wg.Done(); work() }()
wg.Wait()

// Use Channel when: Need results back
results := make(chan int, 3)
go func() { results <- work() }()
go func() { results <- work() }()
go func() { results <- work() }()
for i := 0; i < 3; i++ {
    <-results  // Collect results
}

// Use Context when: Need cancellation/timeout
ctx, cancel := context.WithTimeout(context.Background(), time.Second)
defer cancel()
go func() {
    <-ctx.Done()
    return  // Cancelled!
}()
```

---

## ✅ Summary

| Method | Purpose |
|--------|---------|
| `wg.Add(n)` | Register n tasks to wait for |
| `wg.Done()` | Mark one task complete |
| `wg.Wait()` | Block until all tasks done |
| `defer wg.Done()` | Ensure Done() is called |

**Key pattern:**
```go
var wg sync.WaitGroup

wg.Add(1)
go func() {
    defer wg.Done()  // Always runs on exit
    // ... work ...
}()

wg.Wait()  // Wait for it!
```

---

**WaitGroups are the simplest way to coordinate goroutine completion!**
