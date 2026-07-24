# Lesson 3: Explicit HTTP Server and Timeouts

**Status:** Complete

Lesson 2 used `http.ListenAndServe`, which is excellent for learning the basic
request loop. This lesson replaces that convenience function with an explicit
`http.Server`.

Keep everything in:

```text
cmd/api/main.go
```

Do not create new packages, SQLite, migrations, or SQLC yet.

## Why replace the convenience function?

Conceptually, this:

```text
ListenAndServe(address, handler)
```

creates a basic server and starts it. It is convenient, but it does not give
your code a server value on which to configure production behavior.

An explicit server separates two decisions:

```text
configure the server
        ↓
start the server
```

The configured value owns concerns such as:

- listening address;
- router or root handler;
- request timeouts;
- maximum header size;
- later, graceful shutdown.

## Server versus router

These are different objects:

```text
http.Server
    owns network-facing server behavior
         ↓ sends each accepted request to
http.ServeMux
    chooses the matching route
         ↓ calls
handler
    creates one response
```

The mux does not open a TCP port. The server does not decide which application
route should run. Passing the mux as the server's handler connects them.

## Why timeouts matter

A server shares finite resources among clients:

```text
connections
goroutines
memory
file descriptors
database connections
```

A normal client sends a request promptly. A broken or malicious client might
connect and then send headers one byte at a time, hold the body open, or stop
reading the response.

Without limits:

```text
slow client
    ↓ holds connection
server waits indefinitely
    ↓ enough slow clients
resources become unavailable
```

This family of behavior includes the idea behind a Slowloris attack. Timeouts
turn “wait forever” into “wait for a bounded period.”

## The four timeouts

### Read header timeout

Maximum time allowed to read request headers.

Headers contain the method, path, host, content type, authorization information,
and other request metadata. This is the most important early protection against
clients that send headers extremely slowly.

### Read timeout

Maximum time allowed to read the entire request, including its body.

Be thoughtful with this value later: large uploads legitimately take longer
than small JSON requests.

### Write timeout

Maximum time allowed to write the response.

This prevents a client that does not read responses from holding server
resources forever.

### Idle timeout

Maximum time to wait for the next request on an existing keep-alive connection.

HTTP can reuse one TCP connection for multiple requests. Reuse is efficient, but
an unused connection should not remain open indefinitely.

## Why zero values are dangerous here

Many Go zero values are useful, but a zero server timeout usually means no
timeout. A server that relies on those zero values can wait indefinitely.

Production-oriented programming does not mean choosing perfect numbers on the
first attempt. It means recognizing that the resource policy must be explicit,
measured, and adjusted for the workload.

For this small JSON API, use these learning values:

| Setting | Value |
|---|---:|
| Read-header timeout | 5 seconds |
| Read timeout | 10 seconds |
| Write timeout | 10 seconds |
| Idle timeout | 60 seconds |

These are starting values, not universal laws.

## `time.Duration`

Go represents durations with `time.Duration`.

Constants such as:

```text
time.Second
time.Minute
```

let the code express units directly. Multiplying an integer by `time.Second`
produces a duration, which is clearer and safer than passing an unexplained
integer.

## Your task

Refactor the current server without changing its routes or responses.

Requirements:

1. Keep the existing explicit `ServeMux`.
2. Construct an `http.Server` value.
3. Configure:

   ```text
   address             :8080
   handler             your mux
   read-header timeout 5 seconds
   read timeout        10 seconds
   write timeout       10 seconds
   idle timeout        60 seconds
   ```

4. Start the configured server using its serving method.
5. Report the returned error.
6. Improve the startup message so it includes:

   ```text
   http://localhost:8080
   ```

7. Preserve:

   ```text
   GET /health  → 200 application/json
   POST /health → 405
   unknown path → 404
   ```

Do not add environment configuration or graceful shutdown yet. Each is a
separate concept.

## Observe a real startup failure

With one server already running, try starting a second copy:

```bash
go run ./cmd/api
```

The second process should report that the address is already in use.

This demonstrates:

```text
one TCP address and port
        ↓
one listening socket
        ↓
a second server cannot bind the same pair
```

Stop only the extra attempt. Keep track of which terminal owns the original
server.

## Verify

```bash
go fmt ./...
go vet ./...
go test ./...
go run ./cmd/api
```

From another terminal:

```bash
curl -i http://localhost:8080/health
curl -i -X POST http://localhost:8080/health
curl -i http://localhost:8080/unknown
```

## Questions you should be able to answer

1. What is the difference between `http.Server` and `http.ServeMux`?
2. Why does the server need the mux as its handler?
3. What resource problem do timeouts prevent?
4. What is the difference between read-header and read timeouts?
5. What does idle timeout control?
6. Why are these timeout values not correct for every possible server?
7. Why can only one process listen on `:8080` at a time?

## Stop here

Show:

1. the explicit server configuration;
2. the successful health response;
3. the second-server port-conflict error;
4. the formatter, vet, and test results.

Do not create `internal` packages until this server configuration is reviewed.
