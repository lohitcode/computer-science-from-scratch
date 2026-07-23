# Context, Timeouts, and Cancellation in Go

Concurrent work often needs a way to stop early. A client may disconnect, a request may take too long, or the application may begin shutting down.

Go's `context` package carries cancellation signals, deadlines, and request-scoped values across function boundaries.

This lesson teaches the three main jobs of a context:

```text
context.Context
    |
    +-- cancellation: stop work that is no longer needed
    +-- deadline:     limit how long work may continue
    +-- values:       carry request-scoped metadata
```

The exercise focuses on cancellation and timeouts, but the values section later in this lesson covers the third responsibility.

The cancellation flow is:

```text
caller creates context
        |
        +---- starts work
        |
        +---- timeout expires
                    |
                    v
             cancellation signal
                    |
                    v
              work stops early
```

## Why cancellation is cooperative

Go does not forcefully terminate a goroutine from the outside. The goroutine must cooperate by listening for a cancellation signal and returning.

This design lets the goroutine clean up safely:

- close files;
- release locks;
- stop network operations;
- return a meaningful error;
- avoid leaving partially updated state.

The caller communicates that the work is no longer needed; the worker decides where it is safe to stop.

## The `context.Context` interface

Functions that support cancellation commonly receive a context as their first parameter:

```go
func doWork(ctx context.Context) error
```

By convention:

- name the parameter `ctx`;
- pass it as the first parameter;
- do not store it permanently inside a struct;
- pass it down to other functions performing the same operation.

A context is safe to share between goroutines.

## Starting with a background context

`context.Background()` creates a root context:

```go
parent := context.Background()
```

It has no deadline and is never cancelled by itself. Applications use it as the starting point for creating child contexts.

```text
context.Background()
        |
        +-- context.WithTimeout(...)
        |
        +-- context.WithCancel(...)
        |
        +-- context.WithValue(...)
```

## Creating a timeout

Use `context.WithTimeout` to create a context that automatically expires after a duration:

```go
ctx, cancel := context.WithTimeout(
	context.Background(),
	500*time.Millisecond,
)
defer cancel()
```

It returns two values:

- `ctx` is the new child context;
- `cancel` is a function that manually releases its resources and cancels it early.

The context becomes done when either:

1. the timeout expires; or
2. `cancel()` is called.

## Why call `cancel` when a timeout already exists?

The context may own a timer and related resources until its deadline expires. Calling `cancel` releases them as soon as the operation finishes.

```go
ctx, cancel := context.WithTimeout(parent, timeout)
defer cancel()
```

This is the standard ownership rule: the function that creates a cancellable context is responsible for calling its cancel function.

## The `Done` channel

Every context provides:

```go
ctx.Done()
```

It returns a receive-only channel. The channel is closed when the context is cancelled or its deadline expires.

You do not send a value into this channel:

```text
context active:    ctx.Done() is open
context cancelled: ctx.Done() is closed
```

Receiving from a closed channel proceeds immediately, making it useful inside `select`.

## Waiting for work or cancellation

Suppose an operation takes two seconds:

```go
func slowOperation(ctx context.Context) error {
	select {
	case <-time.After(2 * time.Second):
		return nil
	case <-ctx.Done():
		return ctx.Err()
	}
}
```

The `select` waits for whichever channel becomes ready first:

```text
                      select
                     /      \
       two-second timer      context cancellation
              |                       |
          return nil              return ctx.Err()
```

If the context has a 500-millisecond timeout, cancellation wins before the two-second operation completes.

## Understanding `time.After`

`time.After` returns a channel that receives a value after the specified duration:

```go
case <-time.After(2 * time.Second):
```

The received time value is not needed, so no variable appears on the left side.

For this exercise, the timer represents slow work. In a real application, this branch might instead wait for a database call, HTTP response, or job result.

## Understanding `ctx.Err()`

After `ctx.Done()` is closed, `ctx.Err()` explains why:

```go
err := ctx.Err()
```

The two standard context errors are:

```text
context.Canceled          cancellation was requested manually
context.DeadlineExceeded  the deadline or timeout expired
```

Their displayed messages are:

```text
context canceled
context deadline exceeded
```

Before cancellation, `ctx.Err()` returns `nil`.

## Timeout versus deadline

A timeout is a duration from now:

```go
context.WithTimeout(parent, 500*time.Millisecond)
```

A deadline is a specific time:

```go
deadline := time.Now().Add(500 * time.Millisecond)
context.WithDeadline(parent, deadline)
```

Both produce a context that is cancelled when its time limit is reached. Use a timeout when you care about how long an operation may take; use a deadline when work must finish by a particular moment.

## Manual cancellation

Use `context.WithCancel` when there is no automatic timeout but some event should stop the work:

```go
ctx, cancel := context.WithCancel(context.Background())
defer cancel()
```

Calling:

```go
cancel()
```

closes `ctx.Done()` and causes cooperating functions to stop.

## Contexts form a tree

Derived contexts form parent-child relationships:

```text
Background
    |
    +-- request context
            |
            +-- database timeout
            |
            +-- external API timeout
```

Cancelling a parent cancels all its descendants. Cancelling one child does not cancel its parent or sibling contexts.

This lets an HTTP request control all work performed on its behalf.

## Carrying request-scoped data

You are correct that context is not used only for cancellation. A context can also carry small pieces of metadata that belong to one request or operation.

Typical examples include:

- a request or correlation ID used in logs;
- tracing information;
- authentication information already established for the request;
- metadata that must cross several package or API boundaries.

Create a child context containing a value with `context.WithValue`:

```go
ctx := context.WithValue(parent, key, value)
```

Unlike `WithCancel` and `WithTimeout`, `WithValue` returns only a new context. It does not create a cancel function.

## Context values use keys

A stored value is retrieved using the same key:

```go
value := ctx.Value(key)
```

Conceptually, the context searches from the current child toward its parents:

```text
child context
    |
    +-- has this key? -- yes --> return its value
    |
    +-- no --> search parent
                  |
                  +-- search parent's parent ...
```

If no context in the chain contains that key, `Value` returns `nil`.

## Use a custom key type

Do not use an ordinary string as a context key in reusable code:

```go
// Avoid this.
ctx := context.WithValue(parent, "requestID", "req-123")
```

Another package could independently use the same string and cause a key collision.

Define a private key type instead:

```go
type contextKey string

const requestIDKey contextKey = "requestID"
```

The key's type is part of its identity. A plain string containing `"requestID"` is different from a `contextKey` containing the same text.

The key must be comparable because context compares keys when performing a lookup. Strings, integers, pointers, and structs containing comparable fields can be keys; slices and maps cannot.

## Storing and reading a value

Here is a complete request-ID example:

```go
type contextKey string

const requestIDKey contextKey = "requestID"

func main() {
	parent := context.Background()
	ctx := context.WithValue(parent, requestIDKey, "req-123")

	requestID, ok := ctx.Value(requestIDKey).(string)
	if !ok {
		fmt.Println("request ID is missing")
		return
	}

	fmt.Println("request ID:", requestID)
}
```

`Context.Value` returns `any` because contexts can store values of different types. The type assertion:

```go
requestID, ok := value.(string)
```

checks that the stored value is actually a string.

Using the two-result form prevents a panic when the value is absent or has the wrong type.

## Helper functions make values safer

Larger programs often hide keys and type assertions behind functions:

```go
type contextKey string

const requestIDKey contextKey = "requestID"

func withRequestID(ctx context.Context, id string) context.Context {
	return context.WithValue(ctx, requestIDKey, id)
}

func requestIDFromContext(ctx context.Context) (string, bool) {
	id, ok := ctx.Value(requestIDKey).(string)
	return id, ok
}
```

Callers then use:

```go
ctx := withRequestID(context.Background(), "req-123")

id, ok := requestIDFromContext(ctx)
```

This keeps the key private and gives the value one consistent type.

## Values flow to child contexts

A value stored in a parent is visible through derived child contexts:

```go
parent := context.WithValue(
	context.Background(),
	requestIDKey,
	"req-123",
)

child, cancel := context.WithTimeout(parent, time.Second)
defer cancel()

id, ok := child.Value(requestIDKey).(string)
```

The child carries both pieces of information:

```text
parent
  value: request ID = req-123
        |
        v
child
  inherited value: request ID = req-123
  deadline: one second
```

The parent does not gain values added only to a child. Context information flows down the tree, not back upward.

If a child stores another value using the same key, the child's value takes precedence when looked up through that child. The parent itself remains unchanged.

## Do not use context as a general parameter bag

Context values are intended for request-scoped metadata that crosses process or API boundaries—not ordinary inputs required by a function.

Avoid hiding business data like this:

```go
// Avoid: the function signature hides required inputs.
func calculatePrice(ctx context.Context) int {
	quantity, _ := ctx.Value(quantityKey).(int)
	return quantity * 10
}
```

Use an explicit parameter:

```go
func calculatePrice(ctx context.Context, quantity int) int {
	return quantity * 10
}
```

The explicit signature tells callers and the compiler that `quantity` is required. The context remains available for cancellation, deadlines, tracing, and other request-scoped metadata.

Do not use context values for:

- optional function arguments;
- application configuration;
- database connections;
- loggers that are not request-scoped;
- mutable global state;
- values that can be passed clearly as normal parameters.

## Context values and cancellation work together

One context can carry a deadline, cancellation signal, and request metadata at the same time:

```go
ctx := context.WithValue(
	context.Background(),
	requestIDKey,
	"req-123",
)

ctx, cancel := context.WithTimeout(ctx, 500*time.Millisecond)
defer cancel()
```

Downstream functions can use the request ID for logging while also watching `ctx.Done()` to stop work.

## Connection to HTTP servers

Every incoming Go HTTP request contains a context:

```go
ctx := r.Context()
```

That context is cancelled when appropriate, such as when the client connection closes. Passing it to downstream operations allows unnecessary work to stop:

```go
func handler(w http.ResponseWriter, r *http.Request) {
	ctx := context.WithValue(r.Context(), requestIDKey, "req-123")
	err := loadData(ctx)
	// Handle the result.
}
```

This derived context keeps the HTTP request's original cancellation behavior and adds the request ID. Passing it to `loadData` connects the previous HTTP lesson to both parts of the current context lesson.

## Two context exercises

Context values and context cancellation have different purposes. This chapter therefore uses two sequential exercises:

```text
Problem 19A: middleware + context value
                     |
                     v
Problem 19B: timeout + cancellation
```

Complete 19A first. After it passes, `main.go` will be replaced with the 19B exercise.

## Exercise 19A: Context values in middleware

HTTP middleware is code that runs before or after another handler. Middleware commonly adds request-scoped metadata to a request context.

The flow for this exercise is:

```text
GET /hello
    |
    v
requestIDMiddleware
    |
    +-- read r.Context()
    +-- add request ID "req-123"
    +-- create request carrying the child context
    |
    v
helloHandler
    |
    +-- retrieve request ID
    +-- write "Request ID: req-123"
```

### Middleware shape

Middleware receives one handler and returns another:

```go
func requestIDMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		// Add the context value.
		// Pass the request to next.
	})
}
```

The returned handler wraps `next`. This lets it perform work before calling the next handler.

### Attach a derived context to the request

`context.WithValue` creates a child context, but it does not modify the original HTTP request:

```go
ctx := context.WithValue(r.Context(), requestIDKey, "req-123")
```

Create a request copy carrying that context:

```go
r = r.WithContext(ctx)
```

Then continue the chain:

```go
next.ServeHTTP(w, r)
```

If you pass the original request instead, the next handler cannot see the newly created context.

### Read the value safely in the handler

The handler should retrieve and type-assert the value:

```go
requestID, ok := r.Context().Value(requestIDKey).(string)
if !ok {
	http.Error(w, "request ID missing", http.StatusInternalServerError)
	return
}
```

Then write the successful response using the request ID.

### Register the wrapped handler

Convert the handler function to `http.HandlerFunc`, wrap it, and register it:

```go
handler := http.HandlerFunc(helloHandler)
wrapped := requestIDMiddleware(handler)
http.Handle("/hello", wrapped)
```

This time use `http.Handle`, because the middleware returns an `http.Handler`. In the previous lesson, `http.HandleFunc` accepted a plain handler function.

### Exercise 19A expected response

Run the server, then request:

```bash
curl http://localhost:8080/hello
```

Expected response:

```text
Request ID: req-123
```

## Exercise 19B: Timeout and cancellation

After Exercise 19A is complete, the next version of `main.go` will ask you to create:

```go
func slowOperation(ctx context.Context) error
```

Inside it, you will use `select` to wait for:

- `time.After(2 * time.Second)`, returning `nil`; or
- `ctx.Done()`, returning `ctx.Err()`.

In `main`, you will:

1. Create a context derived from `context.Background()`.
2. Give it a timeout of `500 * time.Millisecond`.
3. Immediately schedule `cancel` with `defer`.
4. Print the starting message.
5. Call `slowOperation(ctx)`.
6. Print the returned context error.

### Exercise 19B expected output

After approximately 500 milliseconds:

```text
Starting slow operation...
Operation stopped: context deadline exceeded
```

The program should finish before the two-second simulated operation completes.

## Important rules for Exercise 19B

### Do not create the context inside the worker

The caller decides how long it is willing to wait. Therefore, `main` creates the timeout and passes the context into `slowOperation`.

### Always call the returned cancel function

Use:

```go
ctx, cancel := context.WithTimeout(...)
defer cancel()
```

Do this even though the timeout will eventually cancel the context automatically.

### Return the context error

When `ctx.Done()` becomes ready, return `ctx.Err()`. Do not invent a different error string; callers may need to distinguish cancellation from a deadline.

### Do not use `time.Sleep` before checking cancellation

This cannot respond early:

```go
time.Sleep(2 * time.Second)
```

The goroutine remains asleep for the full duration. Waiting on a timer and `ctx.Done()` inside the same `select` makes the operation responsive to cancellation.

### Context does not automatically stop arbitrary code

Creating a timeout is not enough. The operation must observe `ctx.Done()` or pass the context to another API that does.

## Useful commands for Exercise 19A

Run from `go-basics`:

```bash
go fmt ./...
go vet ./...
go test ./...
go run .
```

Leave the server running and use another terminal:

```bash
curl http://localhost:8080/hello
```

## Exercise 19A completion checklist

- [ ] A private key type prevents context-key collisions
- [ ] Middleware accepts and returns `http.Handler`
- [ ] `context.WithValue` derives from `r.Context()`
- [ ] `r.WithContext(ctx)` attaches the child context
- [ ] `next.ServeHTTP` continues the middleware chain
- [ ] The handler safely type-asserts the request ID
- [ ] A missing request ID returns an HTTP error
- [ ] The wrapped handler is registered at `/hello`
- [ ] `curl` returns `Request ID: req-123`
- [ ] `go fmt ./...` succeeds
- [ ] `go vet ./...` succeeds
- [ ] `go test ./...` succeeds

## Exercise 19B completion checklist

- [ ] `slowOperation` accepts `context.Context`
- [ ] A `select` waits for both work and cancellation
- [ ] The simulated work lasts two seconds
- [ ] The cancellation branch returns `ctx.Err()`
- [ ] `main` creates a 500-millisecond timeout
- [ ] `cancel` is called with `defer`
- [ ] The returned error is handled and printed
- [ ] The output matches the expected text
- [ ] The program exits after roughly 500 milliseconds
- [ ] `go fmt ./...` succeeds
- [ ] `go vet ./...` succeeds
- [ ] `go test ./...` succeeds

When both exercise checklists pass, Problem 19—and the core Go basics track—is complete.
