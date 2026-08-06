# Checkpoint 17B: Describe Query Contracts to SQLC

Status: **Complete — Stage B**

Started: **2026-08-06 08:05 IST**

Completed: **2026-08-06 08:23 IST**

Wall time: **18m**

## Goal

Translate the three parameterized statements proven in Stage A into a
SQLC-style application query file.

You will learn how:

- SQLC discovers queries through `-- name:` comments;
- the annotation becomes a generated Go method name;
- `:one`, `:many`, `:exec`, and `:execrows` describe result behavior;
- `RETURNING` changes a write from an execution-only query into a row query.

SQLC is not installed or generating Go in this checkpoint. The Go HTTP server
track will configure it against migrations later.

## One Query Definition Has Two Parts

SQLC expects an annotation immediately above ordinary SQL:

```sql
-- name: GetBookByISBN :one
SELECT id, title, isbn
FROM books
WHERE isbn = $1;
```

Read the annotation as:

```text
GetBookByISBN → generated Go method name
:one          → method reads one result row
```

PostgreSQL treats the line as a comment. SQLC reads it as a generation
instruction.

The query file contains only annotations and parameterized SQL. It does not
contain the Stage A testing wrappers:

```text
not in queries.sql → PREPARE, EXECUTE, DEALLOCATE
kept in queries.sql → SELECT/UPDATE, $1 parameters, RETURNING
```

## Choose an Annotation from the Result Contract

### `:one`

Use when the statement is designed to return one row:

```sql
-- name: GetBookByISBN :one
SELECT id, title, isbn
FROM books
WHERE isbn = $1;
```

The generated method returns one row or a no-row error. A unique lookup, such
as customer email in your schema, supports this contract.

### `:many`

Use when zero or more rows are expected:

```sql
-- name: ListBooksByAuthor :many
SELECT id, title
FROM books
WHERE author_id = $1
ORDER BY id;
```

The generated method returns a slice. Even if today's seed data produces one
row, the annotation describes the business relationship: one customer can
have many orders.

### `:exec`

Use for a statement that returns no rows when the caller only needs an error:

```sql
-- name: DeleteBook :exec
DELETE FROM books
WHERE id = $1;
```

### `:execrows`

Use for a no-row statement when the caller also needs the affected-row count:

```sql
-- name: DeleteBooksByAuthor :execrows
DELETE FROM books
WHERE author_id = $1;
```

The count lets code distinguish “nothing matched” from “rows were deleted.”

## `RETURNING` Makes a Write a Row Query

This update produces no result row:

```sql
UPDATE books
SET title = $2
WHERE id = $1;
```

It naturally fits `:exec` or `:execrows`.

This version produces the changed row:

```sql
UPDATE books
SET title = $2
WHERE id = $1
RETURNING id, title;
```

When exactly one changed row is expected, it fits `:one`. Choose the
annotation from what the complete statement returns, not merely from whether
it begins with `SELECT` or `UPDATE`.

## Positional Parameters Stay the Same

Your proven Stage A update used:

```text
$1 → order ID
$2 → product ID
$3 → new quantity
```

Preserve that order in `queries.sql`. SQLC uses the schema and parameter
positions to generate the Go arguments or parameter struct.

SQLC also supports named parameter macros such as `sqlc.arg(name)`. Do not use
them yet; positional parameters keep this stage directly equivalent to your
tested PostgreSQL statements.

## Your Exercise

Leave `main.sql` unchanged. In `queries.sql`, replace the starter comment with
exactly three query definitions.

### 1. Customer lookup

- Annotation: `GetCustomerByEmail :one`
- Copy the underlying `SELECT` from Stage A's `get_customer_by_email` prepared
  statement.
- Keep its explicit columns and `$1` email condition.

### 2. Customer order list

- Annotation: `ListOrdersByCustomer :many`
- Copy the underlying joined `SELECT` from Stage A's
  `list_orders_by_customer` statement.
- Keep the aliases, `$1` customer condition, and deterministic order.

Why `:many`? One customer may own zero, one, or many orders even though Asha
currently has only one.

### 3. Order-item update

- Annotation: `UpdateOrderItemQuantity :one`
- Copy the underlying `UPDATE` from Stage A's
  `update_order_item_quantity` statement.
- Preserve all three parameter positions and the three explicit `RETURNING`
  columns.

Why `:one`? `RETURNING` produces the one updated row identified by the unique
`(order_id, product_id)` pair.

Do not add `PREPARE`, `EXECUTE`, `DEALLOCATE`, `SELECT *`, `RETURNING *`,
`sqlc.arg`, or Go code to `queries.sql`.

## Expected File Shape

```text
-- name: GetCustomerByEmail :one
<parameterized SELECT>

-- name: ListOrdersByCustomer :many
<parameterized joined SELECT>

-- name: UpdateOrderItemQuantity :one
<parameterized UPDATE ... RETURNING>
```

This stage has no new terminal output. The Stage A prepared statements are the
runnable equivalents of these definitions.

## Verify

1. Run `main.sql` twice again to confirm the source queries still work.
2. Say `done`.
3. Codex will compare each statement in `queries.sql` with its proven Stage A
   equivalent and inspect every annotation contract.

## Acceptance Criteria

- `queries.sql` contains exactly three SQL statements.
- Every statement has one correctly formatted `-- name:` annotation.
- Generated method names and commands match the required values exactly.
- SQL bodies remain equivalent to their tested prepared statements.
- All result columns are explicit.
- Positional parameter order is preserved.
- Cardinality annotations match the real business/result shape.
- `main.sql` remains unchanged and rerunnable.

## Official References

- [SQLC query annotations](https://docs.sqlc.dev/en/latest/reference/query-annotations.html)
- [SQLC named parameters](https://docs.sqlc.dev/en/latest/howto/named_parameters.html)

## Stop Here

Say `done` after writing the three definitions. Do not start the final raw-SQL
checkpoint yet.
