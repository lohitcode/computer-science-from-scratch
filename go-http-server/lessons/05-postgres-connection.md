# Lesson 5: Connect the Server to PostgreSQL

**Course progress:** 4 of 12 lessons complete
**Prerequisite:** Raw PostgreSQL track complete (checkpoints 01–18)

You already know PostgreSQL: tables, constraints, joins, transactions, indexes,
query plans, and parameterized application queries. This lesson does **not**
re-teach SQL or the relational model.

It teaches the one thing you have not done yet: reach PostgreSQL from Go
correctly. That means a long-lived connection pool, startup verification, clear
ownership, and a clean package boundary — nothing more.

You will learn the Go-specific concepts below. Skip nothing here even if the
SQL feels obvious.

## What this lesson does not do

- It does not create tables or run migrations.
- It does not write application queries.
- It does not introduce SQLC.
- It does not add graceful HTTP shutdown or authentication.

First establish a correct database connection boundary against PostgreSQL.
Everything else stacks on top of it.

## You know the database; now learn the driver layer

You have run `psql` against PostgreSQL many times. `psql` is one client. Your Go
program is another client, speaking the same wire protocol through a library:

```text
your Go app  ──lib/pq wire protocol──>  PostgreSQL server
```

But Go programs do not usually speak that protocol by hand. The standard library
hides it behind a common API:

```text
application code
      ↓
database/sql            ← Go standard library: handles, pools, contexts
      ↓
driver (pgx)            ← translates database/sql calls into the PG wire protocol
      ↓
PostgreSQL server
```

Two questions fall out of this split, and both shape the code you write.

## `database/sql` is the API; the driver is the implementation

Go's standard library provides `database/sql`. It defines the *concepts* — a
database handle, connections, queries, rows, transactions, pooling,
context-aware operations — but it contains **no PostgreSQL implementation**.

A driver fills that gap. This project uses `pgx`:

```text
github.com/jackc/pgx/v5
```

### Why the driver uses a blank import

Drivers register themselves with `database/sql` during package initialization.
Your code needs that registration side effect, but does not normally call an
exported driver function directly. Go expresses a side-effect-only import with
the blank identifier.

With `pgx`'s standard-library adapter, the registration import is:

```text
github.com/jackc/pgx/v5/stdlib
```

and it registers the driver name:

```text
pgx
```

The mental model:

```text
program imports driver
        ↓
driver initialization runs
        ↓
driver registers name "pgx" with database/sql
        ↓
sql.Open("pgx", dsn) can find that driver
```

Without the blank import, the source may still mention `"pgx"`, but
`database/sql` will not know which implementation owns that name.

## `*sql.DB` is a pool handle, not a connection

This is the single most important concept in this lesson, and the name hides
it. `*sql.DB` is **not** the database, and **not** one connection.

It is a concurrency-safe handle that manages a **pool** of connections:

```text
*sql.DB
├── available connection
├── in-use connection
└── pool-management policy (max open, max idle, lifetime, etc.)
```

Consequences for how you write your app:

- Create **one** long-lived `*sql.DB` at startup and share it across the whole
  application.
- **Never** open a handle per request. That defeats pooling, leaks resources,
  and makes ownership unclear.
- `*sql.DB` is safe for concurrent use — many goroutines (one per HTTP request)
  can use the same handle.

The correct lifetime:

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

This is the same "open once, close once" ownership reasoning you already apply
to files and network listeners. The only new idea is that the handle is a pool.

## `sql.Open` is lazy — that is a trap

This is the second concept that bites people.

`sql.Open(driverName, dataSourceName)` validates its arguments and creates the
handle, but it does **not** necessarily establish a real network connection
immediately. The real connection may happen later, on first use.

So this is **not** proof the database is reachable:

```text
db, err := sql.Open("pgx", dsn)
// err == nil  →  does NOT prove the DB is up
```

If you start serving requests at this point and the DB is actually down, your
"healthy" server will fail on the first real query — the worst time to discover
it.

The fix: **ping with a bounded context during startup.**

```text
sql.Open("pgx", dsn)
    ↓
db.PingContext(ctx)     ← ctx has a deadline
    ↓
reachable → continue startup
unreachable → startup fails now, loudly
```

Failing at startup is far better than reporting "server ready" and discovering
the problem on the first user request. A server that boots but cannot reach its
data is not actually ready.

## The connection string is deployment configuration

You know PostgreSQL connection strings from the database track. As a quick
reminder, the URL form is:

```text
postgres://USER:PASSWORD@HOST:PORT/DBNAME?sslmode=disable
```

For this track, the app reads the whole string from one environment variable:

```text
DATABASE_URL
```

Why one variable rather than separate `PGHOST`, `PGUSER`, etc.? Because the
connection string is a single deployment fact, and treating it as one value keeps
configuration simple and swappable:

```text
local development   postgres://course_user:course_password@localhost:5432/sql_course?sslmode=disable
integration test    postgres://test_user:test_password@localhost:5432/test_db?sslmode=disable
production          postgres://app:••••••@db.internal:5432/app?sslmode=require
```

`sslmode=disable` is right for the local learning container (no TLS configured).
Production typically uses `sslmode=require` or higher.

### Relationship to the database track's variables

Your `databases/compose.yaml` and `.env.example` define separate variables for
the *server container*:

```text
POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_PORT
```

Those configure the PostgreSQL **server** when it boots. `DATABASE_URL` is
different: it is the **client's** instructions for reaching that server. The
values are the same; the role differs. This lesson's application reads only
`DATABASE_URL`.

## The package boundary: `internal/database`

Create one new package:

```text
internal/database/database.go
```

It owns:

```text
driver registration (the blank import lives here)
opening the database
startup connectivity verification (PingContext)
cleanup on failed startup
returning the verified handle
```

It does **not** own:

- HTTP routing;
- environment lookup (the caller passes the DSN in);
- schema creation or migrations;
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

Two reasons the context comes from the caller:

1. It makes the startup deadline explicit and visible in `main`, where process
   lifetime decisions belong.
2. The database package should not secretly choose an unbounded background
   operation. A hang in startup must be bounded by an explicit timeout.

And the DSN comes from the caller (via `config`) for the same reason `PORT`
does: configuration is read once in the config layer and passed down. The
database package does not read the environment itself.

## Error cleanup and ownership

If `sql.Open` creates a handle but `PingContext` fails, the database package
must close that handle before returning the error. Ownership changes only after
a successful return:

```text
database.Open
    ↓
sql.Open succeeds → handle exists
    ↓
PingContext fails
    ↓
database package still owns the handle
    ↓
database package closes it, then returns the error
```

After a successful return:

```text
database package returns the verified handle
    ↓
main now owns it
    ↓
main closes it when the process shuts down
```

This is the same ownership reasoning you used for files and network connections.
Open it, prove it works, hand it off — or clean it up yourself on failure.

## The new composition root

Your startup flow in `main` becomes:

```text
load configuration (PORT + DATABASE_URL)
    ↓
create bounded startup context (5 seconds)
    ↓
open and verify PostgreSQL (internal/database)
    ↓
arrange database close (defer db.Close())
    ↓
construct router
    ↓
construct HTTP server
    ↓
listen
```

### What `/health` should and should not do

Do **not** pass the database into the health handler in this lesson.

The existing `/health` endpoint is a **liveness** check: it proves the HTTP
process can respond. That is a meaningful concept, and it stays unchanged.

A database-dependent **readiness** check ("the server is up *and* can serve real
requests") is a separate concept. It belongs later, once the app has real
database-backed behavior. For now, a successful startup already proved the
database is reachable; `/health` continues to answer without touching it.

Keep the Lesson 4 response exactly:

```text
GET /health → 200 {"status":"ok"}
```

## Your task

### 1. Configuration — `internal/config/config.go`

- Add a `DatabaseURL` field (type `string`) to `Config`.
- Read it from the `DATABASE_URL` environment variable.
- Reject startup when it is missing or empty, using the same strict-error style
  already used for `PORT` (a new exported error in `config`).
- Preserve the existing strict `PORT` validation unchanged.

### 2. Secret hygiene

- The repo already ignores `.env` globally. Before writing `DATABASE_URL` into
  your local `.env`, confirm with `git status --ignored` that it is ignored, not
  untracked.
- Add `go-http-server/.env.example` documenting the variable names **without
  real secrets** (a placeholder DSN). This file is committed; the real `.env`
  is not.

### 3. Dependency

Add the driver when your source imports it:

```bash
go get github.com/jackc/pgx/v5
```

### 4. Database package — `internal/database/database.go`

Create it. It must:

- blank-import `github.com/jackc/pgx/v5/stdlib` for the registration side
  effect;
- export a function that accepts a `context.Context` and a connection string;
- open the `"pgx"` driver via `sql.Open`;
- ping with the supplied context using `db.PingContext`;
- **close the handle if the ping fails** before returning the error;
- return the verified `*sql.DB` on success;
- wrap errors with useful operation context.

It must **not** create tables, run migrations, read the environment, or write
queries.

### 5. Main — `cmd/api/main.go`

- Preserve immediate configuration-error handling.
- Create a 5-second startup context (and call its cancel function).
- Open and verify the database **before** starting HTTP.
- Report a database startup error and stop.
- Close the verified database handle when `main` returns.
- Preserve router and server construction.
- Preserve the `/health` response exactly.

## Verify

### Start PostgreSQL

Reuse the database track's container (it may already be running):

```bash
cd ../databases
docker compose up -d
docker compose ps
```

Wait until `ps` shows the `postgres` service as `healthy`.

### Provide a connection string

From `go-http-server`, put your local DSN in `.env` (Air loads it), for example:

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

### Verify startup actually checks the database (negative test 1)

Prove the ping is real, not ceremonial. Stop PostgreSQL and start the server
again:

```bash
cd ../databases
docker compose stop postgres
cd ../go-http-server
go run ./cmd/api     # should FAIL to start with a database error
```

Then restart PostgreSQL and confirm the server starts cleanly:

```bash
cd ../databases
docker compose start postgres
docker compose ps    # wait for healthy
cd ../go-http-server
go run ./cmd/api
```

### Verify a bad DSN fails startup (negative test 2)

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

1. What is the difference between `database/sql` and the `pgx` driver?
2. Why is the driver imported with `_`?
3. What does `*sql.DB` represent, and why is it not "one connection"?
4. Why should the process create exactly one long-lived `*sql.DB`?
5. Why is `sql.Open` returning no error not proof of connectivity?
6. What does `PingContext` do, and why does it take a context?
7. Who closes the handle when the ping fails? Who closes it after success?
8. Why does the startup context's cancel function still need to be called even
   on the success path?
9. Why does `DATABASE_URL` come from configuration rather than being hardcoded
   in the database package?
10. Why does `/health` stay independent of PostgreSQL in this lesson?

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
