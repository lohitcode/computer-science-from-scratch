# Lesson 2: Your First HTTP Server

**Status:** Complete — HTTP behavior verified

This lesson introduces one HTTP endpoint using Go's standard library.

Keep everything in:

```text
cmd/api/main.go
```

Do not create `internal`, `db`, SQLite, migrations, or SQLC yet. First understand
the complete lifecycle of one HTTP request.

## From a short-lived program to a server

Lesson 1 followed this execution path:

```text
start
  ↓
print message
  ↓
exit
```

An HTTP server is a long-running program:

```text
start
  ↓
create route table
  ↓
listen on a TCP port
  ↓
wait for request
  ↓
run matching handler
  ↓
write response
  ↓
wait for another request
```

The server appears to pause because waiting for requests is its job.

## The three new concepts

### Router

A router matches an incoming method and path with a handler:

```text
GET /health → health handler
```

Use an explicit `http.ServeMux` for this exercise. Passing the mux explicitly
makes the server's routes visible and avoids hidden global route registration.

`ServeMux` means **HTTP request multiplexer**. “Multiplex” means receiving many
possible inputs and directing each one to the correct destination:

```text
incoming requests
├── GET /health       → health handler
├── GET /users/42     → user handler
└── POST /sessions    → session handler
```

`http.NewServeMux()` constructs a new, empty route table owned by your
application. Calling `HandleFunc` adds a pattern-handler pair to that table.

There is also a package-level default mux, used when `nil` is passed as the
server handler. It is convenient for tiny examples, but an explicit mux is
better for a server because:

- the routes are attached to a value you can see and pass;
- tests can construct a fresh router without global state;
- importing another package cannot unexpectedly register application routes;
- separate servers could use separate route tables.

Modern Go route patterns can contain both method and path:

```text
GET /health
```

This lets the mux distinguish two failures:

```text
known path, wrong method  → 405 Method Not Allowed
unknown path              → 404 Not Found
```

A `GET` pattern also permits `HEAD`, because an HTTP `HEAD` request asks for the
same metadata as `GET` without returning the response body.

### Handler

A handler processes one HTTP request.

It receives:

- an `http.ResponseWriter`, used to construct the response;
- an `*http.Request`, containing the incoming request.

Writing to the response writer sends data to the client. Printing with
`fmt.Println` writes only to the server's terminal.

The handler does not return the HTTP response as a Go return value. It builds
the response by calling methods on `ResponseWriter`.

## What `Content-Type: application/json` means

An HTTP response is not just a body. It contains status, headers, and an
optional body:

```text
HTTP/1.1 200 OK
Content-Type: application/json

{"status":"ok"}
```

The bytes in the body do not describe themselves. The client needs metadata to
know whether those bytes represent JSON, plain text, HTML, an image, or
something else. The `Content-Type` header describes that representation.

Media types use this shape:

```text
type/subtype
```

Examples:

```text
text/plain
text/html
application/json
image/png
```

JSON is `application/json`, not `application-json`. The slash separates the
top-level media type from its subtype.

A browser, mobile application, proxy, test client, or API library may use this
header to decide how to parse or display the body. Returning JSON with an
incorrect content type may appear to work in a simple terminal but violates the
HTTP contract and can break stricter clients.

`Content-Type` describes what the server sent. The request header `Accept`
describes what representation the client would prefer to receive. They answer
different questions.

## Why use `encoding/json`

You could manually write a string that resembles JSON, but that becomes unsafe
as soon as values contain quotes, newlines, Unicode, or other characters that
must be escaped.

`json.Encoder` converts Go values into valid JSON and writes the result to the
response writer:

```text
Go map or struct
       ↓ JSON encoder
valid JSON bytes
       ↓ ResponseWriter
HTTP response body
```

The encoder adds a trailing newline. That is valid JSON whitespace, which is
why `curl` may show the prompt on the following line.

### Listener

The HTTP server listens on an address such as:

```text
:8080
```

This means it accepts connections on TCP port `8080`.

`http.ListenAndServe` is a convenience function. It creates a basic HTTP server,
binds the address, and begins the accept-and-serve loop. It normally blocks
because the process must remain available for future requests.

If it returns, something stopped the server or prevented it from starting. That
is why its returned error must not be ignored. Your port-conflict experiment
demonstrated this: a second server could not bind port `8080`.

## Why `/health` comes first

A health endpoint answers a small operational question:

```text
Is the HTTP process running and able to respond?
```

At this stage it should not check SQLite because the server has no database yet.
Later, you can distinguish a basic liveness check from a readiness check that
depends on external resources.

## Your task

Replace the Lesson 1 printing behavior with an HTTP server.

Requirements:

1. Import Go's `net/http` package.
2. Construct an explicit `http.ServeMux`.
3. Register a method-specific route for:

   ```text
   GET /health
   ```

4. Create a health handler with the standard Go handler signature.
5. Set the response `Content-Type` to:

   ```text
   application/json
   ```

6. Return `200 OK` with this JSON:

   ```json
   {"status":"ok"}
   ```

7. Start the server on port `8080`, passing your mux to it.
8. Handle the error returned if the server cannot start or later stops.
9. Print a startup message containing:

   ```text
   http://localhost:8080
   ```

Do not add third-party routing libraries. The standard library is enough for
this checkpoint.

## Header ordering

HTTP headers must be set before the response body is written.

Conceptually:

```text
set headers
    ↓
choose status
    ↓
write body
```

Writing the body may implicitly send `200 OK`, after which changing headers or
status is too late.

## Run the server

From `go-http-server`:

```bash
go run ./cmd/api
```

The command should continue running. Leave it open.

## Test from another terminal

Test the valid request:

```bash
curl -i http://localhost:8080/health
```

Confirm:

- status is `200 OK`;
- content type is `application/json`;
- body represents `{"status":"ok"}`.

Because the route is method-specific, test an unsupported method:

```bash
curl -i -X POST http://localhost:8080/health
```

Expected status:

```text
405 Method Not Allowed
```

Test an unknown route:

```bash
curl -i http://localhost:8080/unknown
```

Expected status:

```text
404 Not Found
```

Stop the server with:

```text
Ctrl+C
```

## Quality checks

After stopping the server:

```bash
go fmt ./...
go vet ./...
go test ./...
```

Then start it once more to ensure formatting did not change behavior:

```bash
go run ./cmd/api
```

## Questions you should be able to answer

1. Why does the server keep running instead of exiting?
2. What does `http.ServeMux` do?
3. What is the difference between `ResponseWriter` and `Request`?
4. Why must `Content-Type` be set before writing the body?
5. Why does `POST /health` return `405` while `/unknown` returns `404`?
6. Why is the mux passed explicitly to the server?

## Stop here

Show:

1. `cmd/api/main.go`;
2. the startup output;
3. the `GET`, `POST`, and unknown-route responses;
4. the output of `go vet ./...` and `go test ./...`.

Do not introduce packages or SQLite until this request flow has been reviewed.
