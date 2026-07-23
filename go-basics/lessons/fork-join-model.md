# The Fork–Join Model in Go

Fork–join is a way to organize concurrent work:

```text
one flow of execution
        |
        | fork
        v
   +----+----+
   |    |    |
 task task task
   |    |    |
   +----+----+
        ^
        | join
        |
continue after every task finishes
```

The parent operation **forks** into multiple independent tasks. At a later synchronization point, it **joins** those tasks by waiting for all of them to finish.

Go does not have `fork` and `join` keywords. It expresses the model using ordinary concurrency tools:

```text
fork  -> `go` statement
join  -> `sync.WaitGroup`, channel receives, or collected results
```

## Why fork–join exists

Sequential code performs one operation at a time:

```text
download A -> download B -> download C -> continue
```

If the operations are independent, they can overlap:

```text
               +-> download A --+
start -> fork -+-> download B --+-> join -> continue
               +-> download C --+
```

Fork–join is useful when:

- work can be divided into independent pieces;
- multiple requests can run concurrently;
- the parent must not continue until every piece finishes;
- results must be collected before the next stage begins.

Examples include processing files, calling independent APIs, resizing images, searching multiple data sources, and dividing CPU-heavy calculations into chunks.

## Forking with goroutines

The `go` keyword starts a function concurrently:

```go
go process("A")
go process("B")
go process("C")
```

Each `go` statement is a fork:

```text
main goroutine
   |
   +-- go process("A") -> goroutine A
   +-- go process("B") -> goroutine B
   +-- go process("C") -> goroutine C
   |
   +-- main continues immediately
```

Starting goroutines is only the fork half of the model. Without a join, `main` may return before the goroutines finish, which terminates the whole program.

## Joining with a `WaitGroup`

A `sync.WaitGroup` tracks unfinished units of work.

```go
var wg sync.WaitGroup

for _, name := range []string{"A", "B", "C"} {
	wg.Add(1)

	go func(name string) {
		defer wg.Done()
		process(name)
	}(name)
}

wg.Wait()
fmt.Println("all work finished")
```

The lifecycle is:

```text
wg counter = 0
      |
      | Add(1), Add(1), Add(1)
      v
wg counter = 3
      |
      | goroutine A calls Done()
      v
wg counter = 2
      |
      | goroutines B and C call Done()
      v
wg counter = 0
      |
      | Wait() unblocks
      v
parent continues
```

`Done()` is equivalent to decreasing the counter by one. `Wait()` blocks until the counter reaches zero.

## The three-part invariant

Every forked unit tracked by a `WaitGroup` must have exactly:

1. one `Add(1)` before it starts;
2. one `Done()` when it finishes;
3. one parent waiting at the join point.

```text
Add(1) --------> goroutine starts --------> Done()
   \                                          /
    +--------------- Wait() ----------------+
```

If the counts do not match:

- too many `Add` calls make `Wait` block forever;
- too many `Done` calls cause a negative-counter panic;
- calling `Add` too late can let `Wait` return before work was registered.

## Add before starting the goroutine

Register the work in the parent:

```go
wg.Add(1)
go worker(&wg)
```

Avoid registering it inside the goroutine:

```go
go func() {
	wg.Add(1) // Too late: the parent may reach Wait first.
	defer wg.Done()
	work()
}()
```

The parent must know that work exists before it waits.

## Why `defer wg.Done()` is common

Put `Done` at the beginning of the goroutine:

```go
go func() {
	defer wg.Done()
	work()
}()
```

The deferred call runs when that goroutine function returns, including through an early return:

```go
go func() {
	defer wg.Done()

	if !valid() {
		return
	}

	work()
}()
```

This makes the completion signal belong to the lifetime of the goroutine.

However, `defer` inside a long-running loop does not run after each iteration. It runs only when the surrounding function returns:

```go
func worker(jobs <-chan Job, wg *sync.WaitGroup) {
	for job := range jobs {
		defer wg.Done() // Delayed until worker returns.
		process(job)
	}
}
```

If the `WaitGroup` counts jobs, call `Done()` at the end of each iteration:

```go
func worker(jobs <-chan Job, wg *sync.WaitGroup) {
	for job := range jobs {
		process(job)
		wg.Done()
	}
}
```

If the `WaitGroup` counts worker goroutines instead, use one deferred `Done` per worker:

```go
func worker(jobs <-chan Job, wg *sync.WaitGroup) {
	defer wg.Done()

	for job := range jobs {
		process(job)
	}
}
```

## What does the counter represent?

This was the central question in the earlier channel exercise. A `WaitGroup` does not know about channels, messages, jobs, or goroutines. Its counter means whatever your program decides it means.

### Model A: count worker goroutines

```go
const workerCount = 3

wg.Add(workerCount)
for i := 0; i < workerCount; i++ {
	go worker(jobs, &wg)
}

close(jobs)
wg.Wait()
```

Here:

```text
counter = number of worker goroutines
one worker exits = one Done()
```

It does not matter whether each worker processes zero, one, or one hundred jobs.

### Model B: count individual jobs

```go
for _, job := range jobs {
	wg.Add(1)
	jobChannel <- job
}

wg.Wait()
```

Here:

```text
counter = number of submitted jobs
one job finishes = one Done()
```

The worker must call `Done()` once per job.

Both models can be correct. The mistake is adding once per job but calling `Done` once per worker, or doing the reverse.

Before writing the code, complete this sentence:

> One count in this `WaitGroup` represents one ______.

Then make every `Add` and `Done` follow that definition.

## Joining with channels

A channel can combine completion and result delivery:

```go
results := make(chan int)

for _, number := range []int{2, 3, 4} {
	go func(n int) {
		results <- n * n
	}(number)
}

for i := 0; i < 3; i++ {
	result := <-results
	fmt.Println(result)
}
```

Each receive joins one forked operation:

```text
3 goroutines forked
        |
        +-- receive result 1
        +-- receive result 2
        +-- receive result 3
        |
all 3 results joined
```

This works when the parent knows exactly how many results to receive.

Use a `WaitGroup` when you only need to wait for completion. Use a channel when you also need to transfer results or coordinate a stream of data. Many programs use both.

## WaitGroup plus a results channel

When many goroutines produce results, a common pattern is:

1. workers send results;
2. a `WaitGroup` tracks workers;
3. a separate goroutine waits and closes the results channel;
4. the parent ranges over results until the channel closes.

```go
results := make(chan int)
var wg sync.WaitGroup

for _, number := range []int{2, 3, 4} {
	wg.Add(1)

	go func(n int) {
		defer wg.Done()
		results <- n * n
	}(number)
}

go func() {
	wg.Wait()
	close(results)
}()

for result := range results {
	fmt.Println(result)
}
```

Why does another goroutine close `results`?

If the parent called `wg.Wait()` before receiving, workers could block while sending to the unbuffered channel:

```text
parent waits for workers
        ^
        |
workers wait for parent to receive
```

That is a deadlock. Letting one goroutine wait and close the channel allows the parent to receive concurrently.

## Fork–join versus worker pools

A direct fork–join starts one goroutine per task:

```text
100 tasks -> 100 goroutines -> wait for all
```

A worker pool starts a fixed number of goroutines and sends many tasks through a channel:

```text
100 tasks -> jobs channel -> 5 workers -> wait for completion
```

Worker pools bound concurrency. This matters when every task consumes a limited resource such as:

- a database connection;
- memory;
- file descriptors;
- API rate limits;
- CPU capacity.

The worker pool still has a fork–join shape, but the forked units may be the long-lived workers rather than individual jobs.

## Concurrency is not always parallelism

Forking creates concurrent goroutines, meaning their executions can overlap in time.

Parallelism means multiple operations are literally executing at the same instant on different CPU cores.

```text
concurrency: tasks make progress during overlapping time
parallelism: tasks execute simultaneously on multiple cores
```

Network and file operations benefit from concurrency because one goroutine can wait while another runs. CPU-heavy work benefits from parallelism when multiple cores are available.

The Go runtime schedules goroutines onto operating-system threads. Your code expresses concurrency; the runtime decides when it can execute that work in parallel.

## Fork–join does not automatically make work faster

Concurrency adds costs:

- goroutine creation and scheduling;
- synchronization;
- channel communication;
- result combination;
- additional complexity and failure paths.

Small or dependent tasks may be faster sequentially:

```text
task B requires task A's result
        |
        +-- cannot run independently
```

Fork only work that is independent enough to benefit.

## Error handling

A `WaitGroup` does not carry errors. It only signals completion.

One standard-library approach is a result channel:

```go
type result struct {
	value int
	err   error
}
```

Each goroutine sends one result, and the parent checks every error while joining.

For production code, cancellation should often accompany errors: when one task fails, the parent may cancel sibling work using `context.Context`.

```text
one child fails
      |
      v
cancel shared context
      |
      v
other children observe ctx.Done() and return
      |
      v
parent joins all children
```

Cancellation requests that work stop; joining confirms that it actually finished. They solve related but different problems.

## Goroutine lifetimes are your responsibility

Go does not automatically join child goroutines when the parent function returns.

```go
func parent() {
	go child()
} // child may still be running
```

A goroutine is not automatically owned by the function that launched it. You must design its lifetime explicitly:

- What causes it to stop?
- Who waits for it?
- Who closes its input channel?
- Can it become blocked forever?
- What happens when its caller is cancelled?

Fork–join answers the waiting question, while channels and contexts usually answer the communication and stopping questions.

## Common mistakes

### Forking without joining

```go
go work()
// main returns immediately
```

### Joining before forking

```go
wg.Wait()
wg.Add(1)
go work()
```

### Copying a `WaitGroup`

Pass its address:

```go
func worker(wg *sync.WaitGroup)
```

Copying it creates different counters that do not coordinate correctly.

### Calling `Done` the wrong number of times

Make the counter represent one clearly defined unit: either a worker, job, request, or another unit—not an accidental mixture.

### Closing a channel from the receiver

The sender that knows no more values will be produced should normally close the channel. Receiving a particular value does not prove that all senders are finished.

### Assuming result order

Concurrent tasks may finish in any order. If ordering matters, include an index in each result and reorder after joining.

## Choosing a join mechanism

| Requirement | Useful mechanism |
|---|---|
| Wait only for completion | `sync.WaitGroup` |
| Receive one result from each task | Channel receives |
| Stream results until producers finish | Channel closed after `WaitGroup.Wait` |
| Stop sibling work after cancellation | `context.Context` plus a join |
| Limit the number of active tasks | Worker pool or semaphore |

## Mental checklist

Before starting concurrent work, answer:

1. What independent work am I forking?
2. What does one `WaitGroup` count represent?
3. Who calls `Done`, and exactly how many times?
4. Where is the join point?
5. How are results and errors returned?
6. How can blocked or unnecessary work stop?
7. Who owns and closes each channel?
8. Does the program require output ordering?

If those answers are explicit, the concurrency design is much less likely to deadlock or leak goroutines.

## Small practice exercise

Write a program that:

1. starts three goroutines;
2. gives each goroutine one integer;
3. calculates the square of that integer;
4. sends a result containing the original index and square;
5. closes the result channel only after all workers finish;
6. collects every result;
7. prints the squares in original input order.

Use:

- a `WaitGroup` to join producers;
- a channel to transfer results;
- an index to restore deterministic ordering.

This combines the entire model:

```text
fork -> calculate concurrently -> communicate -> join -> reorder -> continue
```

## Summary

The Go fork–join model is a design pattern built from several primitives:

```text
go statement       forks concurrent work
WaitGroup          waits for completion
channel            communicates results and may also join
context            requests cancellation or applies a deadline
```

The most important rule is to define the unit being counted. A `WaitGroup` counter does not automatically mean “number of messages” or “number of goroutines.” Your `Add` and `Done` calls give it that meaning.

Forking is easy. Correctly joining, stopping, and collecting results is the real concurrency design work.
