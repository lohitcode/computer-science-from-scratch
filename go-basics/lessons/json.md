# JSON Encoding and Decoding in Go

JSON is a text format used to exchange structured data between programs. Web APIs, configuration files, message queues, and databases commonly use it because many programming languages understand it.

This exercise performs a round trip:

```text
Go struct -> JSON bytes -> Go struct
```

Converting Go data to JSON is called **encoding** or **marshalling**. Converting JSON to Go data is called **decoding** or **unmarshalling**.

## The `encoding/json` package

Go provides JSON support in its standard library:

```go
import "encoding/json"
```

This problem uses two functions:

```go
json.Marshal(value)
json.Unmarshal(data, destination)
```

Both can fail, so both return errors that must be checked.

## Representing JSON with a struct

Consider this JSON object:

```json
{"title":"Go","pages":200}
```

A matching Go struct could be:

```go
type Book struct {
	Title string `json:"title"`
	Pages int    `json:"pages"`
}
```

The field types describe the data:

- `Title` holds JSON text.
- `Pages` holds a JSON number.

The fields begin with capital letters because the JSON package can only process exported struct fields.

## Struct tags

The text after each field is a struct tag:

```go
Title string `json:"title"`
```

It tells the JSON package to use `title` as the JSON key instead of the Go field name `Title`.

```text
Go field       JSON key
Title     <->  "title"
Pages     <->  "pages"
```

Struct tags use backticks, not ordinary quotation marks.

Without a tag, Go would normally encode the exported field using its Go name:

```json
{"Title":"Go"}
```

With the tag, it becomes:

```json
{"title":"Go"}
```

## Encoding with `json.Marshal`

`json.Marshal` takes a Go value and returns JSON as `[]byte`:

```go
book := Book{Title: "Go", Pages: 200}

data, err := json.Marshal(book)
if err != nil {
	fmt.Println("marshal error:", err)
	return
}

fmt.Println(string(data))
```

The returned value is a byte slice because JSON is data that can be written to files or sent over a network. Convert it to `string` when you want to display it as text.

## Decoding with `json.Unmarshal`

`json.Unmarshal` needs:

1. JSON data as `[]byte`.
2. A pointer to the destination where decoded values should be stored.

```go
var decoded Book

err := json.Unmarshal(data, &decoded)
if err != nil {
	fmt.Println("unmarshal error:", err)
	return
}
```

After a successful call, `decoded` contains the values from the JSON.

## Why decoding needs a pointer

`Unmarshal` must modify your variable. Passing `decoded` would give the function only a copy of the struct. Passing `&decoded` gives it the address of the original variable:

```text
decoded variable <---- &decoded ---- json.Unmarshal
       |
       +-- fields are filled here
```

This is the same pointer idea you learned earlier: a function needs an address when it must change the caller's value.

## The round-trip flow

```text
Book struct
    |
    | json.Marshal
    v
JSON []byte
    |
    | json.Unmarshal(data, &decoded)
    v
new Book struct
```

The original and decoded structs are separate values. JSON is the format used to transfer the information between them.

## Your task

Complete `main.go`.

First, define this shape yourself:

```text
Progress
    Name       string, JSON key "name"
    Completed  int,    JSON key "completed"
```

Then:

1. Create a `Progress` value with name `Lohit` and completed count `16`.
2. Marshal it into JSON.
3. Handle the marshal error immediately.
4. Print the JSON with the prefix `JSON: `.
5. Declare a new zero-value `Progress` variable.
6. Unmarshal the JSON into that new variable using a pointer.
7. Handle the unmarshal error immediately.
8. Print the decoded fields in the required format.

## Expected output

```text
JSON: {"name":"Lohit","completed":16}
Decoded: Lohit completed 16 lessons
```

## Important rules

### Struct fields must be exported

This will not be encoded because `name` is unexported:

```go
type Progress struct {
	name string
}
```

Use an exported Go field and a lowercase JSON tag:

```go
Name string `json:"name"`
```

### Pass a pointer to `Unmarshal`

Use:

```go
json.Unmarshal(data, &decoded)
```

The destination must be writable. Forgetting `&` prevents `Unmarshal` from filling your struct and produces an error.

### Check errors before using results

If marshalling fails, do not print or decode the returned data. If unmarshalling fails, do not use the partially decoded struct.

### JSON and Go use different naming conventions

Go exported fields use `PascalCase`, while JSON keys commonly use lowercase or `camelCase`. Struct tags connect the two conventions.

### JSON is not a Go struct's printed representation

Printing a struct directly:

```go
fmt.Println(book)
```

does not produce JSON. Use `json.Marshal` when you need valid JSON.

## Useful commands

Run these commands from `go-basics`:

```bash
go fmt ./...
go vet ./...
go test ./...
go run .
```

## Completion checklist

- [ ] `Progress` has exported `Name` and `Completed` fields
- [ ] Both fields have lowercase JSON tags
- [ ] `json.Marshal` encodes the original struct
- [ ] The marshal error is checked immediately
- [ ] JSON bytes are converted to a string for printing
- [ ] A separate `Progress` value receives the decoded data
- [ ] `json.Unmarshal` receives `&decoded`
- [ ] The unmarshal error is checked immediately
- [ ] The program prints the exact expected output
- [ ] `go fmt ./...` succeeds
- [ ] `go vet ./...` succeeds
- [ ] `go test ./...` succeeds
- [ ] `go run .` succeeds

When every item passes, Problem 17 is complete.
