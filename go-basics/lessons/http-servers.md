# HTTP Servers and Handlers in Go

HTTP is the protocol browsers, mobile applications, and web APIs use to communicate. A client sends a request, and a server sends a response.

```text
client                         Go server
   |                               |
   |  GET /hello HTTP request      |
   |------------------------------>|
   |                               | handler runs
   |  Hello from Go! response      |
   |<------------------------------|
```

Go's standard library includes everything needed to build a basic HTTP server.

## The `net/http` package

Import the HTTP package with:

```go
import "net/http"
```

This exercise uses three important ideas:

- a **handler** processes one request;
- a **route** connects a URL path to a handler;
- a **server** listens for incoming connections.

## Requests and responses

Every HTTP interaction has two sides:

```text
Request
  method: GET
  path:   /hello
  headers and optional body

Response
  status:  200 OK
  headers and optional body
```

In a Go handler, these are represented by:

```go
http.ResponseWriter
*http.Request
```

The request contains information received from the client. The response writer lets your code construct the response sent back to the client.

## The handler function signature

A handler function has this shape:

```go
func exampleHandler(w http.ResponseWriter, r *http.Request) {
	// Handle one request here.
}
```

The parameters have different roles:

- `w` is where you write the response.
- `r` describes the incoming request.

The server calls this function automatically. You do not call it from `main` yourself.

If the request is not needed, Go still requires the parameter because the function must match the handler signature. A valid unused name is `_`:

```go
func exampleHandler(w http.ResponseWriter, _ *http.Request) {
	// This handler does not inspect the request.
}
```

## Writing a response

`http.ResponseWriter` implements Go's writer interfaces, so formatted output can write directly to it:

```go
func exampleHandler(w http.ResponseWriter, _ *http.Request) {
	fmt.Fprintln(w, "Example response")
}
```

Notice the difference:

```go
fmt.Println("text")     // writes to the terminal
fmt.Fprintln(w, "text") // writes to the HTTP response
```

Printing only to the terminal does not send anything to the client.

## Registering a route

A route associates a URL path with a handler:

```go
http.HandleFunc("/example", exampleHandler)
```

After registration, a request to `/example` is sent to `exampleHandler`.

```text
/example request -> route table -> exampleHandler
```

For this problem, register one route:

```text
/hello -> helloHandler
```

Register routes before starting the server.

## Starting the server

Start a server with:

```go
err := http.ListenAndServe(":8080", nil)
```

The address has two pieces:

```text
:8080
  |
  +-- listen on TCP port 8080
```

Passing `nil` tells Go to use the default route table where `http.HandleFunc` registered the handler.

## Why `ListenAndServe` blocks

A server is supposed to keep running and wait for requests. Therefore, `ListenAndServe` does not normally return:

```text
main starts
    |
register route
    |
ListenAndServe
    |
    +-- wait -> request -> handler -> response
    +-- wait -> request -> handler -> response
    +-- wait ...
```

Stop the development server from its terminal with `Ctrl+C`.

## Handling the server error

If `ListenAndServe` returns, the server stopped or failed to start. A common cause is another program already using port 8080.

Handle the returned error:

```go
err := http.ListenAndServe(":8080", nil)
if err != nil {
	fmt.Println("server error:", err)
}
```

Because a normally running server blocks, code after `ListenAndServe` runs only when the server exits.

## Your task

Complete `main.go`:

1. Import `net/http`.
2. Create `helloHandler` using the standard handler signature.
3. Send `Hello from Go!` to the client with `fmt.Fprintln`.
4. Register `helloHandler` at `/hello`.
5. Print `Server listening on http://localhost:8080` to the terminal.
6. Start the server using port `8080` and the default route table.
7. Print the error if `ListenAndServe` returns one.

## Running and testing

Start the server from `go-basics`:

```bash
go run .
```

The first terminal should show:

```text
Server listening on http://localhost:8080
```

It will appear to pause because the server is waiting for requests. Leave it running.

Open a second terminal and send a request:

```bash
curl http://localhost:8080/hello
```

Expected curl output:

```text
Hello from Go!
```

Return to the first terminal and press `Ctrl+C` to stop the server.

## Important rules

### Write the response to `w`

This only prints on the server's terminal:

```go
fmt.Println("Hello from Go!")
```

To answer the client, write to the response writer:

```go
fmt.Fprintln(w, "Hello from Go!")
```

### Register before listening

Call `http.HandleFunc` before `http.ListenAndServe`. Once the server begins listening, execution stays inside the server loop.

### Do not put `ListenAndServe` in a loop

One call already accepts many requests. The HTTP server internally manages the repeated accept-and-handle cycle.

### Port conflicts are external errors

If you see `address already in use`, another process is listening on port 8080. Stop that process or temporarily choose another available port.

### A server has no normal immediate output result

Unlike earlier programs, successful execution does not terminate immediately. Validation requires starting it, sending a request from another process, and then stopping it.

## Useful commands

Before starting the server, run:

```bash
go fmt ./...
go vet ./...
go test ./...
```

Then use two terminals:

```bash
# Terminal 1
go run .

# Terminal 2
curl http://localhost:8080/hello
```

## Completion checklist

- [ ] `helloHandler` has the correct handler signature
- [ ] The handler writes `Hello from Go!` to the response
- [ ] `/hello` is registered with `http.HandleFunc`
- [ ] The listening message is printed before the server starts
- [ ] `http.ListenAndServe` uses `:8080`
- [ ] The error returned by `ListenAndServe` is handled
- [ ] `go fmt ./...` succeeds
- [ ] `go vet ./...` succeeds
- [ ] `go test ./...` succeeds
- [ ] `curl http://localhost:8080/hello` returns the expected text

When every item passes, Problem 18 is complete.
