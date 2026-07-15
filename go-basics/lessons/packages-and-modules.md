# Packages and Modules in Go

You have completed Problem 12: goroutines, channels, and WaitGroups. This problem teaches you how to organize a Go program across directories and reuse code.

## The mental model

A **function** organizes statements. A **package** organizes related Go files and functions. A **module** organizes the packages that belong to one project.

```text
Module: go-basics
├── Package: main
│   └── main.go
└── Package: calculator
    └── calculator.go
```

| Concept | Meaning | Example |
|---|---|---|
| Function | A reusable operation | `Add(5, 3)` |
| Package | Related Go code in one directory | `calculator/` |
| Module | The project and its import namespace | `go-basics` |
| Import | Makes another package available | `"go-basics/calculator"` |

## What `go.mod` does

Run this once from the `go-basics` directory:

```bash
go mod init go-basics
```

This creates `go.mod`:

```go
module go-basics
```

The module name becomes the beginning of imports for your own packages. Therefore, the `calculator` directory is imported as:

```go
import "go-basics/calculator"
```

The module name does not need to match the directory name, although using the same name is convenient while learning. Published modules commonly use a repository path such as `github.com/username/project`.

## Packages and directories

Every `.go` file begins with a package declaration:

```go
package calculator
```

Normally, all ordinary Go files in the same directory must declare the same package. The package name usually matches the directory name.

`package main` is special: it creates an executable program. A `main` package needs a `main()` function as its entry point.

## Exported and private names

Go uses capitalization to control visibility:

```go
func Add(a, b int) int { // Exported: usable by other packages
	return a + b
}

func validate(a int) { // Private: usable only inside calculator
}
```

There is no `public` keyword. A name beginning with an uppercase letter is exported; a lowercase name is private to its package.

## Your exercise

Start from this structure:

```text
go-basics/
├── go.mod
├── main.go
└── calculator/
    └── calculator.go
```

### Step 1: Initialize the module

```bash
cd go-basics
go mod init go-basics
```

### Step 2: Create the calculator package

Create `calculator/calculator.go` and begin with:

```go
package calculator
```

Implement these exported functions yourself:

```go
func Add(a, b int) int
func Subtract(a, b int) int
func Multiply(a, b int) int
```

### Step 3: Import and call it

Add your local package to the import block in `main.go`:

```go
import (
	"fmt"
	"go-basics/calculator"
)
```

Call all three functions with `5` and `3`.

### Step 4: Run and verify

```bash
go fmt ./...
go run .
```

Expected output:

```text
Packages & Modules!
5 + 3 = 8
5 - 3 = 2
5 * 3 = 15
```

## Why `go run .`?

The dot means “build and run the package in the current directory.” As a project grows, this is more natural than naming individual source files.

Useful commands:

```bash
go run .       # Compile and run the current main package
go build .     # Compile an executable
go test ./...  # Test every package in this module
go fmt ./...   # Format every package in this module
go mod tidy    # Remove unused dependencies and add required ones
```

## Common errors

### `package ... is not in std`

Check that `go.mod` exists, the import starts with the exact module name, and the package directory exists.

### `undefined: calculator.add`

Rename `add` to `Add`. Lowercase identifiers are not exported.

### `found packages calculator and main in the same directory`

Keep `package calculator` files inside `calculator/` and `package main` files in the project root.

### Import cycle

Packages cannot import each other in a circle. `main` may import `calculator`, but `calculator` should not import `main`.

## Completion checklist

- [ ] `go.mod` exists and declares `module go-basics`
- [ ] `calculator/calculator.go` declares `package calculator`
- [ ] `Add`, `Subtract`, and `Multiply` are exported
- [ ] `main.go` imports `go-basics/calculator`
- [ ] `go fmt ./...` succeeds
- [ ] `go run .` prints the expected results

When every box is satisfied, Problem 13 is complete.
