# Files and I/O in Go

I/O means input and output. Reading a file brings data into your program; writing a file sends data from your program to storage.

In this problem, your program will perform a round trip:

```text
Go string -> bytes -> notes.txt -> bytes -> Go string
```

## The `os` package

Go's standard `os` package provides functions for working with the operating system, including files.

Import it with:

```go
import "os"
```

This exercise uses two functions:

```go
os.WriteFile(name, data, permission)
os.ReadFile(name)
```

Both operations can fail, so both return errors that must be checked.

## Bytes and text

Files store bytes. A Go `string` represents text, while `[]byte` represents a slice of bytes.

Convert text to bytes when writing:

```go
text := "hello"
data := []byte(text)
```

Convert bytes back to text after reading:

```go
text := string(data)
```

These conversions produce the following flow:

```text
"hello" -- []byte(...) --> [104 101 108 108 111]
   ^                              |
   +-------- string(...) <--------+
```

## Writing an entire file

`os.WriteFile` has this general shape:

```go
err := os.WriteFile(filename, data, permission)
```

For example:

```go
message := []byte("example text")
err := os.WriteFile("example.txt", message, 0644)
if err != nil {
	fmt.Println("write error:", err)
	return
}
```

If the file does not exist, `WriteFile` creates it. If it already exists, `WriteFile` replaces its contents.

## File permissions

The value `0644` describes the permissions to use when creating the file:

```text
owner:  read + write
group:  read
others: read
```

The leading zero marks this as an octal number. Octal permission values are conventional on Unix-like systems.

For this exercise, use:

```go
0644
```

## Reading an entire file

`os.ReadFile` returns the file's contents and an error:

```go
data, err := os.ReadFile("example.txt")
if err != nil {
	fmt.Println("read error:", err)
	return
}

fmt.Println(string(data))
```

The returned `data` has type `[]byte`. Convert it to a string before printing it as text.

## Why file operations return errors

Even correct Go syntax cannot guarantee that an I/O operation succeeds. For example:

- the file may not exist;
- the program may lack permission;
- the disk may be full;
- part of the path may be invalid.

Errors make these external failures visible to your program.

## Handle each operation immediately

Check each error directly after the operation that produced it:

```text
write file
    |
    +-- error? --> report and return
    |
    +-- success --> read file
                        |
                        +-- error? --> report and return
                        |
                        +-- success --> print contents
```

Do not wait until the end to check errors. If writing fails, trying to read the expected file may produce a second, less useful error.

## Your task

Complete `main.go` so that it:

1. Creates a `[]byte` containing `Learning Go files!`.
2. Writes those bytes to `notes.txt` using permission `0644`.
3. Checks the write error and returns if writing failed.
4. Reads `notes.txt` using `os.ReadFile`.
5. Checks the read error and returns if reading failed.
6. Converts the read bytes to a string and prints them.

## Expected output

```text
Learning Go files!
```

After a successful run, `notes.txt` should exist inside the directory from which you ran the program.

## Important rules

### The working directory controls the path

`"notes.txt"` is a relative path. It means a file named `notes.txt` inside the program's current working directory.

If you run the command from `go-basics`:

```bash
go run .
```

the file will be created at `go-basics/notes.txt`.

### Do not ignore errors

Avoid discarding an error with `_`:

```go
data, _ := os.ReadFile("notes.txt")
```

Without checking the error, your program cannot distinguish an empty file from a failed read.

### Return after a failure

Printing an error does not stop the function. Use `return` afterward so the program does not continue with invalid data.

### Keep the operations in order

Write the file before reading it. Otherwise, the first run may try to read a file that does not exist yet.

## Useful commands

Run these commands from `go-basics`:

```bash
go fmt ./...
go vet ./...
go run .
```

You can inspect the created file with:

```bash
cat notes.txt
```

## Completion checklist

- [ ] The program imports `os`
- [ ] The message is converted to `[]byte`
- [ ] `os.WriteFile` writes `notes.txt` with permission `0644`
- [ ] The write error is checked immediately
- [ ] `os.ReadFile` reads `notes.txt`
- [ ] The read error is checked immediately
- [ ] The read bytes are converted to a string
- [ ] The program prints `Learning Go files!`
- [ ] `go fmt ./...` succeeds
- [ ] `go vet ./...` succeeds
- [ ] `go run .` prints the expected output

When every item passes, Problem 16 is complete.
