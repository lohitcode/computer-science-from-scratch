# Lesson 1: Start a Go Server Project

**Status:** Complete

This lesson teaches only the first project boundary: a Go module containing one
executable command.

Do not create `internal`, `db`, SQLite, migrations, or SQLC yet. Those will be
introduced one at a time after this checkpoint works.

## Why begin here?

A production server eventually contains HTTP, configuration, database access,
migrations, generated SQLC code, authentication, and tests. If all of those are
introduced together, an error could come from any layer.

First prove this smaller execution path:

```text
go command
    ↓
find go.mod
    ↓
compile package main
    ↓
call func main
    ↓
print one message
```

## Module, package, and command

A **module** is the group of Go packages governed by one `go.mod`.

A **package** is a directory of Go files compiled together.

A **command** is an executable package named `main` that contains a `main`
function.

The first project structure should be only:

```text
go-http-server/
├── cmd/
│   └── api/
│       └── main.go
├── lessons/
│   └── 01-module-and-command.md
└── go.mod
```

`cmd` is a convention for grouping executables. `api` is the name of this
executable. Later, the same project could have another command such as a
background worker without mixing its startup code with the API server:

```text
cmd/
├── api/
└── worker/
```

Do not create the worker now.

## Step 1: Initialize the module

From the repository root:

```bash
cd go-http-server
go mod init github.com/lohitcode/computer-science-from-scratch/go-http-server
```

The module path becomes the prefix for imports created later.

There should be only one `go.mod` for this server. Do not initialize another
module inside `cmd`.

## Step 2: Create the command

Create:

```text
cmd/api/main.go
```

The file must:

- declare `package main`;
- contain a `main` function;
- print exactly `Hello from Go HTTP server!`.

Do not import `net/http` yet. This checkpoint is about module and command
structure, not HTTP.

## Verify

From `go-http-server`:

```bash
go fmt ./...
go vet ./...
go test ./...
go run ./cmd/api
```

Expected program output:

```text
Hello from Go HTTP server!
```

## Before asking for the next lesson

You should be able to answer:

1. What boundary does `go.mod` create?
2. Why is the executable under `cmd/api`?
3. What makes a package an executable command?
4. Is the filename `main.go` required, or is it a convention?

## Stop here

Show `go.mod`, `cmd/api/main.go`, and the command output. After the implementation
is reviewed, the next lesson will introduce one HTTP health endpoint. It will
not introduce SQLite or SQLC yet.
