# Checkpoint 18D: Define the Application Query Contracts

Status: **Complete**

Started: **2026-08-06 16:37 IST**

Completed: **2026-08-06 16:49 IST**

Wall time: **12m**

## Goal

Finish the raw PostgreSQL checkpoint by expressing three realistic bookstore
operations as parameterized, SQLC-compatible query contracts.

This stage adds no new syntax. It tests whether you can combine parameters,
joins, deterministic ordering, `RETURNING`, and SQLC cardinality annotations
without a prepared solution.

## Think from the Caller's Contract

Before writing SQL, describe what the future Go method needs:

```text
method input → SQL parameter positions
method result → selected or returned columns
cardinality  → :one, :many, :exec, or :execrows
```

For example, an inventory application might define:

```sql
-- name: ListWarehouseProducts :many
SELECT p.id, p.name, s.quantity
FROM stock AS s
JOIN products AS p ON p.id = s.product_id
WHERE s.warehouse_id = $1
ORDER BY p.id;
```

Why `:many`? A warehouse can contain zero, one, or many products. The current
seed-row count does not change that business relationship.

An update that returns its uniquely targeted row can use `:one`:

```sql
-- name: UpdateStockQuantity :one
UPDATE stock
SET quantity = $3
WHERE warehouse_id = $1
  AND product_id = $2
RETURNING warehouse_id, product_id, quantity;
```

The compound predicate identifies the row; mutable `quantity` does not.

## Your Exercise

Leave `main.sql` unchanged. Replace the old contents of `queries.sql` with
exactly these three bookstore query contracts, in this order.

### 1. Find one book by ISBN

- Annotation: `GetBookByISBN :one`
- Input: `$1` is the ISBN.
- Start from `books`.
- Return exactly `id`, `isbn`, `title`, and `price_paise` in that order.
- Filter by the unique `isbn` column.

### 2. List the items in one order

- Annotation: `ListOrderItems :many`
- Input: `$1` is the order ID.
- Start from `order_items AS oi`.
- Join `books AS b` using their key relationship.
- Return these expressions in this exact order:

```text
oi.order_id
b.title AS book_title
oi.quantity
oi.unit_price_paise
```

- Filter with `oi.order_id = $1`.
- Order by `b.id` so the result is deterministic.

Why `:many`? One order can contain zero, one, or many items.

### 3. Update one order-item quantity

- Annotation: `UpdateOrderItemQuantity :one`
- `$1` is the order ID.
- `$2` is the book ID.
- `$3` is the new quantity.
- Update `order_items.quantity`.
- Target the row using both stable key columns—not its current quantity.
- Return exactly `order_id`, `book_id`, and `quantity` in that order.

Why `:one`? The schema's unique `(order_id, book_id)` constraint allows at
most one matching row, and `RETURNING` produces that changed row.

## Expected File Shape

Your file must have exactly this structural shape:

```text
-- name: GetBookByISBN :one
<parameterized SELECT>

-- name: ListOrderItems :many
<parameterized joined SELECT with ORDER BY>

-- name: UpdateOrderItemQuantity :one
<parameterized UPDATE with RETURNING>
```

Do not include `PREPARE`, `EXECUTE`, `DEALLOCATE`, hard-coded runtime values,
`SELECT *`, `RETURNING *`, Go code, or extra queries.

## Expected Behavior

When SQLC is configured later, these definitions are intended to generate
methods shaped like:

```text
GetBookByISBN(isbn)                         → one book or a no-row error
ListOrderItems(orderID)                     → zero or more order-item rows
UpdateOrderItemQuantity(orderID, bookID, q) → one updated row or a no-row error
```

There is no new terminal result for `queries.sql` in this raw-SQL stage.
Checkpoint 17 already proved how the equivalent parameterized statements run
through PostgreSQL. Here, correctness is the query-file contract itself.

## Verify

1. Run `main.sql` twice and ensure the Stage C output remains unchanged.
2. Inspect `queries.sql`: it must contain exactly three statements and three
   immediately preceding `-- name:` annotations.
3. Say `done`. Codex will inspect every parameter position, join, selected
   column, annotation, and result contract.

## Acceptance Criteria

- `main.sql` remains unchanged and rerunnable.
- `queries.sql` contains exactly three statements.
- Each statement has one correctly formatted SQLC annotation.
- Method names and cardinality commands match the required contracts.
- Every runtime value uses its required positional parameter.
- The item-list join follows the declared foreign key.
- The many-row query has deterministic ordering.
- The update targets the unique `(order_id, book_id)` pair.
- All selected and returned columns are explicit and correctly ordered.
- No testing wrappers, wildcard columns, hard-coded inputs, or extra queries
  are present.
