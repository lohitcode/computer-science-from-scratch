# Unit Testing in Go

A unit test checks one small piece of code automatically. Instead of running the program and inspecting its output yourself, you describe the expected result in code and let Go verify it.

## Why tests matter

Suppose `Add(2, 3)` should return `5`. You can check it manually once, but the code may change later. A test records that rule permanently:

```text
input:    Add(2, 3)
expected: 5
actual:   value returned by Add
```

If the actual value differs from the expected value, the test fails and reports the problem.

## Go's built-in testing tools

Go includes testing support in the standard library. You do not need to install another package.

A test file must:

1. End with `_test.go`.
2. Import the `testing` package.
3. Contain functions whose names begin with `Test`.
4. Give each test function the parameter `t *testing.T`.

The basic shape is:

```go
func TestSomething(t *testing.T) {
	// Arrange the input.
	// Act by calling the function.
	// Assert that the result is correct.
}
```

`go test` discovers these functions automatically. You do not call them from `main`.

## Arrange, act, assert

A useful mental model for a test has three stages:

```go
func TestMultiply(t *testing.T) {
	// Arrange
	a, b := 3, 4

	// Act
	got := Multiply(a, b)

	// Assert
	want := 12
	if got != want {
		t.Errorf("Multiply(%d, %d) = %d; want %d", a, b, got, want)
	}
}
```

The common names `got` and `want` make failures easy to understand:

- `got` is what the code returned.
- `want` is what the test expected.

## Failing a test

The test parameter `t` controls the current test.

Use `t.Errorf` when you want to report a failure and allow the test function to continue:

```go
t.Errorf("got %d; want %d", got, want)
```

Use `t.Fatalf` when continuing would be unsafe or meaningless:

```go
if err != nil {
	t.Fatalf("unexpected error: %v", err)
}
```

`Fatalf` reports the failure and stops only the current test, not the entire test suite.

## Testing a successful error-returning function

For a function returning `(value, error)`, test both values:

```go
got, err := someOperation()
if err != nil {
	t.Fatalf("unexpected error: %v", err)
}

if got != want {
	t.Errorf("got %d; want %d", got, want)
}
```

Check the error first. If an unexpected error occurred, the result may not be useful.

## Testing an expected error

Some inputs are supposed to produce an error. In that case, a `nil` error means the test should fail:

```go
_, err := someFailingOperation()
if err == nil {
	t.Fatal("expected an error, got nil")
}
```

After confirming that `err` is not `nil`, you can safely check its message:

```go
want := "expected message"
if err.Error() != want {
	t.Errorf("error = %q; want %q", err.Error(), want)
}
```

Do not call `err.Error()` before checking `err == nil`. Calling a method through a nil error value can cause a panic.

## Your task

Complete the three TODOs in `calculator/calculator_test.go`:

1. `TestAdd` checks that `Add(2, 3)` returns `5`.
2. `TestDivide` checks that `Divide(10, 2)` returns `5` and `nil`.
3. `TestDivideByZero` checks that `Divide(10, 0)` returns an error with the exact message `cannot divide by zero`.

Each test should have this signature:

```go
func TestName(t *testing.T)
```

Once you add real test functions, delete this temporary line from the starter file:

```go
var _ *testing.T
```

It exists only to prevent an unused-import compiler error before you begin.

## Running tests

Run these commands from `go-basics`:

```bash
go fmt ./...
go vet ./...
go test ./...
```

For detailed test names and results, use:

```bash
go test -v ./...
```

Go may show `(cached)` when neither the code nor the tests have changed. Force a fresh run with:

```bash
go test -count=1 ./...
```

## Reading a failure

A failure might look like:

```text
--- FAIL: TestDivideByZero
    calculator_test.go:30: error = "Cannot divide by 0"; want "cannot divide by zero"
FAIL
```

This tells you:

- which test failed;
- the source line that reported the failure;
- the actual value (`got`);
- the expected value (`want`).

The test should guide you to the production-code bug. Fix the implementation when its behavior violates the required contract; do not weaken a correct requirement merely to make the test pass.

## Important rules

### Test behavior, not internal steps

Call the exported function and inspect what it returns. A test should not depend on how the function performs its calculation internally.

### Keep tests independent

Each test should prepare its own inputs. One test should not need another test to run first.

### Make failures descriptive

Include the actual and expected values in failure messages. A message such as `test failed` does not explain what went wrong.

### Tests are regular Go code

Tests must compile. Normal rules still apply: imports must be used, variables must be used, and code must be formatted.

## Completion checklist

- [ ] `TestAdd` passes
- [ ] `TestDivide` checks both the result and error
- [ ] `TestDivideByZero` first checks for a non-`nil` error
- [ ] The zero-division error message is checked exactly
- [ ] The temporary `var _ *testing.T` line is removed
- [ ] `go fmt ./...` succeeds
- [ ] `go vet ./...` succeeds
- [ ] `go test -v ./...` reports all three tests as passing

When every item passes, Problem 15 is complete.
