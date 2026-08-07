# Lesson 5: Connect the Server to PostgreSQL

**Course progress:** 4 of 12 lessons complete

The server currently loses all application state when the process exits, and it
has no way to share state across requests or restarts. This lesson introduces
persistence by opening one long-lived connection pool to a PostgreSQL database
when the server starts.

You will learn:

- why an application uses a database that runs as a separate process;
- how a Go program reaches PostgreSQL over the network;
- the relationship between `database/sql` and a database driver;
- why `sql.Open` does not prove a connection works;
- what `*sql.DB` actually represents;
- why the connection string is deployment configuration, like `PORT`;
- how startup and shutdown should own the database handle;
- why secrets must never be committed.

This lesson does not create tables, run migrations, write queries, introduce
SQLC, add graceful HTTP shutdown, or build authentication. First establish a
correct database connection boundary against PostgreSQL.

## Memory disappears; persistent data remains

Values in Go variables live only while the process is running:

```text
start server
    ↓
create Go values in memory
    ↓
stop server
    ↓
memory is released
```

A database stores state outside the process, so it survives restarts:

```text
server process ──writes──> PostgreSQL
      stops
new process    ───reads──> same PostgreSQL
```

Later, users and sessions will survive server restarts because their records
will live in the database rather than only in maps or slices.

## PostgreSQL is a separate process, not a file

Unlike an embedded database such as SQLite, PostgreSQL is a server. It runs as
its own long-lived process and owns its own files:

```text
PostgreSQL server process
├── manages data files on disk
├── accepts network connections
├── enforces SQL, constraints, transactions
└── authenticates clients
```

Your Go application is a *client* of that server. It reaches PostgreSQL across
the network, exactly as one process talks to another:

```text
Go server ──network (TCP)──> PostgreSQL server ──> data files
```

This has real consequences for this lesson:

- the server must already be running and reachable before your app starts;
- the app must authenticate, so connection details include credentials;
- the app must tolerate the network failing between client and server.

You already have a PostgreSQL server from the database track. This lesson reuses
it instead of adding new infrastructure.

## The connection string is deployment input

To connect, the client must tell the driver four things at minimum:

```text
who     user
what    password
where   host and port
which   database name
```

These are deployment facts, not program logic. The same binary should run against
a local database during development and a different database in production
without being rebuilt, exactly like `PORT`:

```text
local development   DATABASE_URL=postgres://course_user:course_password@localhost:5432/sql_course?sslmode=disable
integration test    DATABASE_URL=postgres://test_user:test_password@localhost:5432/test_db?sslmode=disable
production          DATABASE_URL=postgres://app:••••••@db.internal:5432/app?sslmode=require
```

The program stays the same; its input changes.

For this track, represent all connection details as a single environment
variable:

```text
DATABASE_URL
```

A PostgreSQL connection string (DSN) has a URL form:

```text
postgres://USER:PASSWORD@HOST:PORT/DBNAME?sslmode=disable
```

`sslmode=disable` is appropriate for the local learning container, which has no
TLS configured. Production typically uses `sslmode=require` or higher.

### Relationship to the database track's variables

The database track's `compose.yaml` and `.env.example` define separate variables
for the *server container*:

```text
POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_PORT
```

Those configure the PostgreSQL server when it boots. `DATABASE_URL` is different:
it is the *client's* instructions for reaching that server. The values are the
same; the role differs. This lesson's application reads only `DATABASE_URL`.

## Go separates database API from database driver

Go's standard library provides:

```text
database/sql
```

It defines common database concepts — handles, connections, queries, rows,
transactions, connection pooling, and context-aware operations. It does not
contain a PostgreSQL implementation.

A driver translates the common `database/sql` operations into the wire protocol
of one specific database:

```text
your application
      ↓
database/sql
      ↓
PostgreSQL driver
      ↓
PostgreSQL server
```

This project will use the `pgx` driver:

```text
github.com/jackc/pgx/v5
```

It is a modern, actively maintained pure-Go driver for PostgreSQL.

## Why the driver uses a blank import

Database drivers register themselves with `database/sql` during package
initialization. Your code needs that registration side effect, but it does not
normally call an exported driver function directly. Go expresses a
side-effect-only import with the blank identifier.

With `pgx`'s standard-library adapter, the registration import is:

```text
github.com/jackc/pgx/v5/stdlib
```

and it registers the driver name:

```text
pgx
```

The mental model is:

```text
program imports driver
        ↓
driver initialization runs
        ↓
driver registers name "pgx"
        ↓
sql.Open can find that driver
```

Without the import, the source may still mention `"pgx"`, but `database/sql`
will not know which implementation owns that name.

## `sql.Open` is intentionally lazy

The name can be misleading. `sql.Open` validates arguments and creates a
database handle, but it does not necessarily establish a real network connection
immediately.

Conceptually:

```text
sql.Open
    ↓
create configured database handle
    ↓
real connection may happen later
```

Therefore this is not enough to prove startup connectivity:

```text
Open returned no error
```

Use a context-aware ping during startup:

```text
Open
  ↓
PingContext with timeout
  ↓
database is reachable or startup fails
```

Failing during startup is better than reporting "server ready" and discovering
the database problem on the first user request. A server that boots but cannot
reach its data is not actually ready.

## What `*sql.DB` really is

Despite its name, `*sql.DB` is not the database itself and not one permanent
connection. It is a concurrency-safe handle that manages a pool of connections:

```text
*sql.DB
├── available connection
├── in-use connection
└── connection-management policy
```

Create one long-lived handle during application startup and share it with the
parts of the application that need database access.

Do not do this for every request:

```text
request
  ↓
sql.Open
  ↓
query
  ↓
Close
```

Repeatedly constructing handles defeats pooling, leaks resources, and makes
ownership unclear.

The correct lifetime is:

```text
process starts
    ↓
open and verify *sql.DB once
    ↓
serve many requests using it
    ↓
process shuts down
    ↓
close *sql.DB once
```

## Secrets must never be committed

`DATABASE_URL` contains a password. The lesson that adds it must also make sure
it cannot be committed by accident.

Process-local configuration such as a `.env` file is convenient for development,
but it is runtime input, not source. Confirm the repository ignores `.env`
*before* you put credentials in it:

```text
.env            runtime secrets; ignore
.env.example    documented non-secret template; commit
```

The rule:

```text
if it contains a real password, it must be ignored, not tracked
```

## The database package boundary

Create:

```text
internal/database/database.go
```

The package owns:

```text
driver registration
opening the database
startup connectivity verification
cleanup on failed startup
returning the verified handle
```

It does not own:

- HTTP routing;
- environment lookup (the caller passes the connection string in);
- schema creation;
- migrations;
- user queries;
- JSON responses.

Its exported operation should conceptually accept:

```text
startup context
connection string (DSN)
```

and return:

```text
verified *sql.DB
or an error
```

Passing the context from the caller makes the startup deadline explicit. The
database package should not secretly choose an unbounded background operation.

Passing the DSN from the caller keeps environment reading in the configuration
layer, where `PORT` already lives. Configuration is read once and passed down;
the database package does not read the environment itself.

## Why startup needs a timeout context

An external network operation should not be allowed to hang process startup
forever:

```text
main creates startup context with deadline
        ↓
database.Open receives context
        ↓
PingContext observes deadline
        ↓
success or bounded failure
```

Use a short learning timeout, such as five seconds. The exact production value
depends on the environment.

The caller that creates a derived context must also call its cancellation
function so timer resources are released promptly.

## Error cleanup and ownership

If `sql.Open` creates a handle but `PingContext` fails, the database package
must close that handle before returning the error. Ownership changes only after
success:

```text
database package opens handle
        ↓
ping fails
        ↓
database package still owns it
        ↓
database package closes it
```

After a successful return:

```text
database package returns handle
        ↓
main/application now owns it
        ↓
main/application closes it at shutdown
```

This is the same ownership reasoning used for files and network connections.

## Update the composition root

The startup flow becomes:

```text
load configuration
    ↓
create bounded startup context
    ↓
open and verify PostgreSQL
    ↓
arrange database close
    ↓
construct router
    ↓
construct HTTP server
    ↓
listen
```

Do not pass the database into the health handler yet. The existing `/health`
endpoint is a *liveness* check: it proves the HTTP process can respond.

A database-dependent *readiness* endpoint is a separate concept that will be
introduced when the application has database-backed behavior. For now, a
successful startup already proved the database is reachable; `/health` continues
to answer without touching it.

## Your task

### Configuration

- Add a `DatabaseURL` field to `config.Config` (type `string`).
- Read it from the `DATABASE_URL` environment variable.
- Reject startup when it is missing or empty, using the same strict-error style
  already used for `PORT` (a new exported error in `config`).
- Preserve the existing strict `PORT` validation unchanged.

### Secret hygiene

- Ensure `.env` files are ignored by the repository (check `git status --ignored`
  after editing your local `.env`; it must appear as ignored, not untracked).
- Add a `go-http-server/.env.example` that documents the variable names *without
  real secrets* (for example a placeholder DSN). This file is committed; the
  real `.env` is not.

### Dependency

Add the driver when your source imports it:

```bash
go get github.com/jackc/pgx/v5
```

### Database package

Create `internal/database/database.go`.

It must:

- accept a context and a connection string (DSN);
- open the `"pgx"` driver via `sql.Open`;
- ping with the supplied context using `PingContext`;
- close the handle if the ping fails;
- return the verified `*sql.DB` on success;
- wrap errors with useful operation context.

It must not create tables or execute migrations. It must not read the
environment.

### Main

- Preserve immediate configuration-error handling.
- Create a five-second startup context (and call its cancel function).
- Open and verify the database before starting HTTP.
- Report a database startup error and stop.
- Close the verified database handle when `main` returns.
- Preserve router and server construction.
- Preserve the `/health` response exactly.

## Verify

### Start PostgreSQL

Reuse the database track's container:

```bash
cd ../databases
docker compose up -d
docker compose ps
```

Wait until `ps` shows the `postgres` service as `healthy`.

### Provide a connection string

From `go-http-server`, put your local DSN in a `.env` that Air (or your shell)
will load, for example:

```text
PORT=8080
DATABASE_URL=postgres://course_user:course_password@localhost:5432/sql_course?sslmode=disable
```

If you are not using Air, export the variables in your shell instead:

```bash
export PORT=8080
export DATABASE_URL='postgres://course_user:course_password@localhost:5432/sql_course?sslmode=disable'
```

### Run the server

```bash
go run ./cmd/api
```

Expected: the server starts, the startup ping succeeds, and you see the existing
listening message.

Test the endpoint:

```bash
curl -i http://localhost:8080/health
```

The response must be unchanged from Lesson 4:

```text
HTTP/1.1 200 OK
Content-Type: application/json

{"status":"ok"}
```

### Verify startup actually checks the database

Prove the ping is real, not ceremonial. Stop PostgreSQL and start the server
again:

```bash
cd ../databases
docker compose stop postgres
cd ../go-http-server
go run ./cmd/api     # should fail to start with a database error
```

Then restart PostgreSQL and confirm the server starts cleanly again:

```bash
cd ../databases
docker compose start postgres
docker compose ps    # wait for healthy
cd ../go-http-server
go run ./cmd/api
```

### Verify a bad DSN fails startup

With PostgreSQL running, give an invalid `DATABASE_URL` (wrong database name or
bad credentials) and confirm the server refuses to start.

### Check Git hygiene

```bash
git status --short --ignored
```

Your real `.env` must appear as ignored, never as untracked or staged. Confirm
no password is about to be committed.

### Quality checks

```bash
go mod tidy
go fmt ./...
go vet ./...
go test ./...
go list ./...
```

The package list should now include:

```text
internal/database
```

## Questions you should be able to answer

1. What survives after the Go process exits?
2. How is PostgreSQL different from an embedded database like SQLite?
3. Why is the application a *client* of PostgreSQL?
4. What responsibility belongs to `database/sql`?
5. What responsibility belongs to the `pgx` driver?
6. Why is the driver imported as a blank import?
7. Why is `sql.Open` not a connectivity check?
8. What does `*sql.DB` represent, and why should the process create only one?
9. Why is `DATABASE_URL` configuration rather than a hardcoded constant?
10. Why does `PingContext` receive a context?
11. Who closes the handle when the ping fails? Who closes it after success?
12. Why must `.env` be ignored while `.env.example` is committed?
13. Why does `/health` remain independent of PostgreSQL in this lesson?

## Stop here

Show:

1. the updated `Config` (with `DatabaseURL`) and its new validation error;
2. `go-http-server/.env.example`;
3. the ignored (not tracked) real `.env`;
4. `internal/database/database.go`;
5. the startup composition in `main`;
6. the unchanged `/health` response;
7. the server **refusing** to start when PostgreSQL is down or the DSN is wrong;
8. formatter, vet, tests, and package-list output.

Do not create database tables, migration files, graceful HTTP shutdown, or SQLC
configuration until this connection lifecycle is reviewed.

## Official references

- [Go database access overview](https://go.dev/doc/database/)
- [Opening a database handle](https://go.dev/doc/database/open-handle)
- [`database/sql`](https://pkg.go.dev/database/sql)
- [`pgx` driver](https://pkg.go.dev/github.com/jackc/pgx/v5)
- [PostgreSQL connection strings](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNSTRING)
