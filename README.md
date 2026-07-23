# Software Engineering From Scratch

A hands-on journey toward becoming a well-rounded software engineer by learning programming, computer science, systems, backend engineering, and production practices from first principles.

This repository records both the lessons and the code written while learning. Each track progresses through small exercises that are explained, implemented, verified, and committed before moving forward.

## Current Progress

### Completed foundations

- **C basics** — memory, pointers, structs, allocation, and low-level programming
- **Go basics** — packages, interfaces, concurrency, testing, files, JSON, HTTP, middleware, and context

### Other tracks in progress

- **Python basics** — language fundamentals and common Python patterns
- **FastAPI foundations** — API basics and CRUD application structure
- **FastAPI CRUD** — database-backed API practice

### Current track

- **Data Structures & Algorithms with Go**
  - complexity analysis
  - arrays and slices
  - searching and sorting
  - linked structures
  - stacks and queues
  - hash tables
  - trees, heaps, and graphs

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
| [`dsa-go/`](dsa-go/) | Data structures, algorithms, and complexity | Current |
| [`databases/`](databases/) | Persistent data, SQL, indexes, and transactions | Planned |
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
cd dsa-go
go run .
```

See [`dsa-go/lessons/big-o-and-linear-search.md`](dsa-go/lessons/big-o-and-linear-search.md) before beginning the first DSA problem.

The complete course sequence is in the
[`dsa-go` track index](dsa-go/README.md).
