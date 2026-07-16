# Error Handling in Go

Go functions can return errors as ordinary values. This makes failure visible in the function signature and requires the caller to decide what to do.

## The problem

Your calculator currently has functions such as:

```go
func Add(a, b int) int
```

Addition always produces an integer, but integer division is not valid when the divisor is zero. Returning only an integer would give the caller no reliable way to distinguish a valid result from a failure.

## Multiple return values

A Go function can return more than one value:

```go
func operation() (int, error)
```

The two returned values represent different information:

```text
result: the successful answer
error:  what prevented success
```

The convention is:

| Outcome | Result | Error |
|---|---:|---|
| Success | useful value | `nil` |
| Failure | zero value | non-`nil` error |

`nil` means there is no error.

## The `error` interface

Go has a built-in `error` type. Conceptually, an error is any value that provides this method:

```go
Error() string
```

For this exercise, create a simple error using the standard `errors` package:

```go
import "errors"

err := errors.New("cannot divide by zero")
```

Error messages conventionally begin with a lowercase letter and do not end with punctuation because callers may add context around them.

## Handling an error

Receive both returned values:

```go
result, err := someOperation()
```

Check the error before using the result:

```go
if err != nil {
	fmt.Println("Error:", err)
	return
}

fmt.Println("Result:", result)
```

This is called an early return: handle the failure first, then continue along the successful path.

## Your task

Add one exported function to `calculator/calculator.go`:

```go
func Divide(a, b int) (int, error)
```

Its contract is:

1. If `b` is zero, return `0` and an error containing `cannot divide by zero`.
2. Otherwise, return `a / b` and `nil`.

Think through the two paths before coding:

```text
Divide(a, b)
    |
    +-- Is b zero? -- yes --> zero result + error
    |
    +-- no ----------------> quotient + nil
```

Then update `main.go` to call:

```go
calculator.Divide(10, 2)
calculator.Divide(10, 0)
```

Handle each returned error explicitly.

## Expected output

```text
Error Handling!
10 / 2 = 5
Error: cannot divide by zero
```

## Important rules

### Check the error first

Do not use a result until you know the operation succeeded:

```go
result, err := calculator.Divide(10, 2)
if err != nil {
	// Handle failure
}

// Use result here
```

### Do not use an error string as the result

Keep the numerical result and failure information separate. That is why the function returns `(int, error)` instead of a string.

### Do not panic for an expected failure

Division by zero is an input problem that the caller can handle. Return an error instead of terminating the whole program with `panic`.

### Do not ignore errors

This compiles, but throws away important information:

```go
result, _ := calculator.Divide(10, 0)
```

The blank identifier `_` intentionally discards a value. Avoid it when the error matters.

## Useful commands

Run these commands from `go-basics`:

```bash
go fmt ./...
go vet ./...
go run .
```

## Completion checklist

- [ ] `Divide` returns `(int, error)`
- [ ] A zero divisor returns a non-`nil` error
- [ ] Valid division returns the quotient and `nil`
- [ ] `main.go` checks both errors
- [ ] `go fmt ./...` succeeds
- [ ] `go vet ./...` succeeds
- [ ] `go run .` prints the expected output

When every item passes, Problem 14 is complete.
