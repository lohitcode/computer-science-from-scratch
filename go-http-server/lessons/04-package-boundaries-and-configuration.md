# Lesson 4: Package Boundaries and Configuration

**Status:** Complete

The current server works. That is exactly when refactoring becomes useful:
behavior is known, so you can move responsibilities and verify that nothing
changed.

This lesson introduces:

- Go package boundaries;
- the special `internal` directory;
- dependency direction;
- a small composition root;
- environment-based configuration.

It does not introduce SQLite, migrations, SQLC, authentication, or third-party
packages.

## Begin with the current problem

`cmd/api/main.go` currently does several jobs:

```text
main
├── chooses configuration
├── builds the route table
├── implements the health handler
├── configures HTTP timeouts
├── starts the listener
└── reports server failure
```

This is not wrong for a tiny program. It becomes difficult when users,
authentication, SQLite, and SQLC arrive because every new concern would be
added to the same file.

The goal is not “make `main.go` short” as an aesthetic rule. The goal is to make
ownership and dependency direction visible.

## One directory is one package

In Go, a directory normally represents a package:

```text
internal/config/
└── config.go       → package config

internal/httpserver/
├── router.go       → package httpserver
└── server.go       → package httpserver
```

Files in the same directory belong to the same package and are compiled
together. Splitting `router.go` and `server.go` makes the source easier to
navigate, but it does not create two packages because both files remain in the
same directory.

Moving code into another directory creates a real package boundary:

```text
cmd/api            package main
internal/config    package config
internal/httpserver package httpserver
```

To use an exported name from another package, the importing package refers to
it through the package name:

```text
config.Load
httpserver.NewRouter
httpserver.NewServer
```

Names beginning with a capital letter are exported from their package. Lowercase
names remain private to that package.

## Why `internal` is different

`cmd` is a convention. `internal` is enforced by the Go toolchain.

Given:

```text
go-http-server/internal/httpserver
```

packages inside the `go-http-server` parent tree may import it. An unrelated Go
module outside that permitted tree cannot.

This expresses:

```text
The HTTP server package is an implementation detail of this application,
not a public library that other repositories should depend on.
```

That freedom matters. You can reorganize application internals without
maintaining compatibility for unknown external importers.

## Package ownership

Create only these packages:

```text
go-http-server/
├── cmd/
│   └── api/
│       └── main.go
└── internal/
    ├── config/
    │   └── config.go
    └── httpserver/
        ├── router.go
        └── server.go
```

### `config` owns configuration

The configuration package answers:

```text
What settings should this process use?
Are required settings present and valid?
```

For now, it owns only:

```text
HTTP port
```

Later, the same configuration value can contain the database path and
environment mode.

It should not:

- start the server;
- register routes;
- open the database;
- print HTTP responses.

### `httpserver/router.go` owns HTTP routing

The router file answers:

```text
Which method and path call which handler?
```

For now, it owns:

```text
GET /health
```

It should construct and return a `*http.ServeMux`. Returning the concrete mux
allows the composition root to register more feature routes later before
passing it to the server as an `http.Handler`.

### `httpserver/server.go` owns server policy

The server file answers:

```text
Which port is used?
Which handler receives requests?
What timeout policy protects the server?
```

It should create an `http.Server` using:

- the port supplied by the caller;
- the router supplied by the caller;
- the timeout values learned in Lesson 3.

It should not read environment variables itself. Configuration is supplied to
it.

### `cmd/api/main.go` owns composition and process lifetime

`main` becomes the composition root:

```text
load configuration
       ↓
construct router
       ↓
construct server with configuration + router
       ↓
print startup information
       ↓
start server
       ↓
report process-ending error
```

“Composition root” means the one place where concrete application parts are
created and connected.

## Dependency direction

The desired import direction is:

```text
cmd/api
├── imports internal/config
└── imports internal/httpserver

internal/httpserver
└── imports standard-library HTTP packages

internal/config
└── imports standard-library environment packages
```

Neither internal package imports `cmd/api`. Application packages should not
depend on the executable that assembles them.

This produces a directed dependency graph:

```text
main ──> config
  │
  └────> httpserver
```

Go rejects import cycles:

```text
package A imports package B
package B imports package A
```

The restriction forces packages to have a clear dependency direction instead
of becoming mutually entangled.

## Configuration is input

The listening port is currently hardcoded:

```text
:8080
```

Hardcoding means changing behavior requires editing, rebuilding, and redeploying
the program.

Environment configuration allows the same binary to run in different
environments:

```text
local development  PORT=8080
integration test   PORT=18080
deployment         PORT=8000
```

The program stays the same; its input changes.

## `Getenv` versus `LookupEnv`

Go provides two related ideas:

```text
Getenv
    returns a string
    missing and explicitly empty both appear as ""

LookupEnv
    returns the value plus whether the variable exists
```

For this lesson, an empty or missing `PORT` is a startup error. Requiring the
deployment input makes configuration mistakes visible immediately instead of
silently choosing a different port.

For a future secret such as a signing key, “missing” and “present but empty”
may both be fatal configuration errors rather than reasons to use a default.

Defaults are appropriate for safe local settings. Production secrets should
not receive convenient hardcoded defaults.

## Configuration should be loaded once

Avoid this:

```text
router reads environment
database reads environment
auth service reads environment
handler reads environment
```

That hides dependencies and makes tests depend on global process state.

Prefer:

```text
environment
    ↓ read once
Config value
    ↓ passed explicitly
main constructs application
```

After startup, the rest of the application receives ordinary Go values.

## A useful configuration shape

Your config package needs a small exported structure conceptually shaped like:

```text
Config
└── Port string
```

Its loader should:

1. look for `PORT`;
2. reject a missing, empty, non-numeric, or out-of-range value;
3. accept ports from `1` through `65535`;
4. return the validated configuration.

Do not add a `.env` parsing library. The program reads the process environment.
A shell, Air, Docker, or deployment system may populate it later.

## Preserve behavior while refactoring

A refactor changes structure without intentionally changing external behavior:

```text
before:
GET /health → 200 {"status":"ok"}

after:
GET /health → 200 {"status":"ok"}
```

If the response changes during this lesson, that is a regression, not part of
the package refactor.

## Your task

Create:

```text
internal/config/config.go
internal/httpserver/router.go
internal/httpserver/server.go
```

Refactor with these responsibilities:

### Configuration

- Export a configuration type containing `Port`.
- Export a loader.
- Read `PORT`.
- Fail when it is absent, empty, non-numeric, or outside `1` through `65535`.

### Router

- Export a router constructor.
- Create an explicit `ServeMux`.
- Register `GET /health`.
- Preserve `Content-Type: application/json`.
- Preserve `{"status":"ok"}`.
- Return the constructed `*http.ServeMux`.

### Server

- Export a server constructor.
- Accept the port and handler as arguments.
- Return a configured `*http.Server`.
- Preserve all four Lesson 3 timeout values.

### Main

- Load configuration once.
- Construct the router.
- Construct the server with the port and router.
- Print the actual configured port before listening.
- Start the server.
- Report the returned error.

Do not add SQLite, SQLC, graceful shutdown, third-party packages, or generic
`utils` packages.

## Verify missing configuration fails

Run without `PORT`:

```bash
env -u PORT go run ./cmd/api
```

The process should report the configuration error and must not start listening.

## Verify configured startup

Run:

```bash
PORT=8080 go run ./cmd/api
```

Expected port:

```text
:8080
```

From another terminal:

```bash
curl -i http://localhost:8080/health
```

## Verify configuration changes behavior

Stop the first server, then run:

```bash
PORT=9090 go run ./cmd/api
```

Test:

```bash
curl -i http://localhost:9090/health
```

Also confirm the old address is no longer serving this process:

```bash
curl -i --max-time 2 http://localhost:8080/health
```

## Inspect the package graph

From `go-http-server`:

```bash
go list ./...
```

You should see packages for:

```text
cmd/api
internal/config
internal/httpserver
```

This demonstrates that directories define Go packages.

## Quality checks

```bash
go fmt ./...
go vet ./...
go test ./...
```

## Questions you should be able to answer

1. Why is `cmd` a convention while `internal` is enforced?
2. What package owns the `GET /health` route?
3. What package owns timeout policy?
4. Why should the HTTP server package not read `PORT` directly?
5. What is a composition root?
6. Why does `*http.ServeMux` satisfy the `http.Handler` interface?
7. Why does Go reject import cycles?
8. What is the difference between configuration and application behavior?
9. Why should configuration be read once?
10. Why must the endpoint response remain unchanged during this refactor?

## Stop here

Show:

1. the new three-file package structure;
2. `cmd/api/main.go`;
3. the missing-`PORT` startup failure;
4. the server running on `:9090`;
5. `go list ./...`;
6. formatter, vet, and test output.

Do not introduce SQLite until these package boundaries are reviewed.
