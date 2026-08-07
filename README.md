# Software Engineering From Scratch

A hands-on journey toward becoming a well-rounded software engineer by learning programming, computer science, systems, backend engineering, and production practices from first principles.

This repository records both the lessons and the code written while learning. Each track progresses through small exercises that are explained, implemented, verified, and committed before moving forward.

## Current Progress

### Completed foundations

- **C basics** — memory, pointers, structs, allocation, and low-level programming
- **Go basics** — packages, interfaces, concurrency, testing, files, JSON, HTTP, middleware, and context
- **PostgreSQL raw SQL** — tables, constraints, joins, transactions, indexes, query plans, and parameterized application queries

### Other tracks in progress

- **Python basics** — language fundamentals and common Python patterns
- **FastAPI foundations** — API basics and CRUD application structure
- **FastAPI CRUD** — database-backed API practice
- **Production Go HTTP server** — module structure, routing, `/health`, timeouts, and environment configuration (lessons 1–4 complete)

### Current track

- **Production Go HTTP server → PostgreSQL** — opening a long-lived connection pool, startup verification, and graceful ownership; then versioned migrations and SQLC

## Engineering Roadmap

```text
programming foundations
        |
        v
data structures and algorithms
        |
        v
operating systems + networking
        |
        v
databases + backend engineering
        |
        v
testing + debugging + tooling
        |
        v
distributed systems
        |
        v
production software projects
```

Machine learning may be explored later as a specialization. The primary goal is broad, transferable software-engineering ability.

## Repository Tracks

| Track | Purpose | Status |
|---|---|---|
| [`c-basics/`](c-basics/) | Low-level programming and memory fundamentals | Complete |
| [`python-basics/`](python-basics/) | Python language foundations | In progress |
| [`go-basics/`](go-basics/) | Go and backend-concurrency foundations | Complete |
| [`fastapi-basics/`](fastapi-basics/) | Python HTTP API foundations | In progress |
| [`fastapi-crud/`](fastapi-crud/) | Database-backed API practice | In progress |
| [`dsa-go/`](dsa-go/) | Data structures, algorithms, and complexity | In progress |
| [`databases/`](databases/) | Persistent data, SQL, indexes, and transactions | Complete |
| [`go-http-server/`](go-http-server/) | Production Go HTTP server connected to PostgreSQL | Current |
| [`networking/`](networking/) | Protocols, packets, HTTP, and network debugging | Planned |
| [`operating-systems/`](operating-systems/) | Processes, memory, files, and concurrency | Planned |
| [`system-design/`](system-design/) | Scalable and reliable system architecture | Planned |
| [`security/`](security/) | Threats, trust, authentication, and secure software | Planned |
| [`deployment/`](deployment/) | Delivery, containers, observability, and operations | Planned |
| [`production-projects/`](production-projects/) | Complete production-quality software projects | Planned |

## Learning Method

Each problem follows the same feedback loop:

```text
read the concept
      |
      v
implement one focused problem
      |
      v
format + analyze + test + run
      |
      v
understand failures
      |
      v
commit and continue
```

Conceptual guides live in each track's `lessons/` directory. The current exercise remains in that track's main source file unless the concept specifically requires multiple files.

## Current Exercise

```bash
cd go-http-server
go run ./cmd/api
```

See [`go-http-server/lessons/05-postgres-connection.md`](go-http-server/lessons/05-postgres-connection.md) for the next server lesson: connect the Go server to PostgreSQL.
