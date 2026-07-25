# Lesson 5: Connect the Server to SQLite

**Course progress:** 4 of 12 lessons complete

The server currently loses all application state when the process exits. This
lesson introduces persistence by opening one local SQLite database when the
server starts.

You will learn:

- why applications use a database;
- what SQLite is;
- the relationship between `database/sql` and a database driver;
- why `sql.Open` does not prove a connection works;
- what `*sql.DB` actually represents;
- where a local database file belongs;
- how startup and shutdown should own the database handle.

This lesson does not create tables, run migrations, write queries, or introduce
SQLC. First establish a correct database connection boundary.

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

A database stores state outside the process:

```text
server process ──writes──> app.db
      stops
new process    ───reads──> same app.db
```

Later, users and sessions will survive server restarts because their records
will live in the database rather than only in maps or slices.

## Why SQLite?

SQLite is an embedded relational database. Unlike PostgreSQL or MySQL, it does
not require a separate database-server process for this project.

```text
PostgreSQL-style setup:
Go server ──network──> database server ──> database files

SQLite setup:
Go server ──library calls──> local app.db file
```

SQLite still provides SQL, tables, indexes, constraints, and transactions. Its
simple deployment model makes it excellent for learning and for applications
that run as one server instance with a moderate write workload.

SQLite is not “just a text file.” The SQLite library controls the binary
database format, locking, transactions, and durability.

## Go separates database API from database driver

Go's standard library provides:

```text
database/sql
```

It defines common database concepts:

- database handles;
- connections;
- queries;
- rows;
- transactions;
- connection pooling;
- context-aware operations.

It does not contain an SQLite implementation.

A driver translates the common `database/sql` operations into behavior for one
specific database:

```text
your application
      ↓
database/sql
      ↓
SQLite driver
      ↓
SQLite database file
```

This project will use:

```text
modernc.org/sqlite
```

It is a pure-Go SQLite driver, so building the project does not require a C
compiler or CGo.

## Why the driver uses a blank import

Database drivers register themselves with `database/sql` during package
initialization.

Your code needs the driver's initialization side effect, but does not normally
call an exported driver function directly. Go expresses a side-effect-only
import with the blank identifier:

```text
_ "modernc.org/sqlite"
```

The mental model is:

```text
program imports driver
        ↓
driver initialization runs
        ↓
driver registers name "sqlite"
        ↓
sql.Open can find that driver
```

Without the import, the source may still mention `"sqlite"`, but
`database/sql` will not know which implementation owns that name.

## `sql.Open` is intentionally lazy

The name can be misleading. `sql.Open` normally validates arguments and creates
a database handle, but it may not immediately establish a real connection or
touch the database file.

Conceptually:

```text
sql.Open
    ↓
create configured database handle
    ↓
real connection may happen later
```

Therefore, this is not enough to prove startup connectivity:

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

Failing during startup is better than reporting “server ready” and discovering
the database problem on the first user request.

## What `*sql.DB` really is

Despite its name, `*sql.DB` is not the database itself and not necessarily one
permanent connection.

It is a concurrency-safe handle that manages a pool of database connections:

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

Repeatedly constructing database handles defeats pooling and makes ownership
unclear.

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

## Where the database file belongs

Create a runtime data directory:

```text
db/
└── data/
    └── app.db
```

Later, source-controlled SQL will use separate directories:

```text
db/
├── data/         runtime state; do not commit
├── migrations/   schema history; commit
└── queries/      handwritten SQLC input; commit
```

These represent different things:

```text
app.db       current runtime data
migrations   instructions that create/change schema
queries      operations the application performs
```

For now, create only `db/data`. Do not create empty migration or query files.

## Git hygiene for SQLite

SQLite may create companion files:

```text
app.db
app.db-wal
app.db-shm
```

They are runtime state and should not be committed.

Extend `.gitignore` for:

```text
db/data/*.db
db/data/*.db-wal
db/data/*.db-shm
```

The database directory must exist before SQLite can create a file inside it.
SQLite can create `app.db`; it cannot create a missing chain of parent
directories for you.

## Add the database path to configuration

The validated deployment input remains:

```text
PORT
```

For this learning server, add a code-owned database path to the configuration
value:

```text
Config
├── Port
└── DatabasePath
```

Use:

```text
db/data/app.db
```

as the current database path. Do not introduce another environment variable in
this lesson.

This demonstrates that configuration can combine:

- environment-supplied values such as the deployment port;
- application defaults such as the local database location.

If deployment later requires a mounted path, the source of `DatabasePath` can
change without changing the database package's API.

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
- environment lookup;
- schema creation;
- migrations;
- user queries;
- JSON responses.

Its exported operation should conceptually accept:

```text
database path
startup context
```

and return:

```text
verified *sql.DB
or an error
```

Passing the context from the caller makes the startup deadline explicit. The
database package should not secretly choose an unbounded background operation.

## Why startup needs a timeout context

An external operation should not be allowed to hang process startup forever:

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

## Error cleanup

If `sql.Open` creates a handle but `PingContext` fails, the database package
must close that handle before returning the error.

Ownership changes only after success:

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
open and verify SQLite
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
endpoint is a liveness check: it proves the HTTP process can respond.

A database-dependent readiness endpoint is a separate concept that will be
introduced when the application has database-backed behavior.

## Your task

### Configuration

- Add `DatabasePath` to `config.Config`.
- Set it to `db/data/app.db`.
- Preserve the existing strict `PORT` validation.

### Filesystem

- Create `db/data/`.
- Ignore SQLite database and companion files.

### Dependency

Add the driver when your source imports it:

```bash
go get modernc.org/sqlite
```

### Database package

Create `internal/database/database.go`.

It must:

- accept a context and database path;
- open the `"sqlite"` driver;
- ping with the supplied context;
- close the handle if ping fails;
- return the verified `*sql.DB` on success;
- wrap errors with useful operation context.

It must not create tables or execute migrations.

### Main

- Preserve immediate configuration-error handling.
- Create a five-second startup context.
- Open and verify the database before starting HTTP.
- Report a database startup error and stop.
- Close the verified database handle when `main` returns.
- Preserve router and server construction.
- Preserve the `/health` response.

## Verify

Start without a database file:

```bash
rm -f db/data/app.db db/data/app.db-wal db/data/app.db-shm
PORT=8080 go run ./cmd/api
```

The server should start and SQLite should create:

```text
db/data/app.db
```

Test:

```bash
curl -i http://localhost:8080/health
```

Stop the server, start it again, and confirm the same database file is reused.

Check Git:

```bash
git status --short --ignored
```

The database file should appear as ignored, not untracked.

Run:

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
2. How is SQLite different from a separate database server?
3. What responsibility belongs to `database/sql`?
4. What responsibility belongs to the SQLite driver?
5. Why is the driver imported with `_`?
6. Why is `sql.Open` not a connectivity check?
7. What does `*sql.DB` represent?
8. Why should the process create one long-lived database handle?
9. Why does `PingContext` receive a context?
10. Who closes the handle when ping fails?
11. Who closes it after successful startup?
12. Why is `app.db` ignored while future migrations will be committed?
13. Why does `/health` remain independent of SQLite in this lesson?

## Stop here

Show:

1. the updated `Config`;
2. `internal/database/database.go`;
3. the startup composition in `main`;
4. the created and ignored `app.db`;
5. the working `/health` response;
6. formatter, vet, tests, and package-list output.

Do not create database tables, migration files, or SQLC configuration until
this connection lifecycle is reviewed.

## Official references

- [Go database access overview](https://go.dev/doc/database/)
- [Opening a database handle](https://go.dev/doc/database/open-handle)
- [`database/sql`](https://pkg.go.dev/database/sql)
- [SQLC SQLite tutorial and driver choice](https://docs.sqlc.dev/en/latest/tutorials/getting-started-sqlite.html)
