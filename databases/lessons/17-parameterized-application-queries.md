# Checkpoint 17A: Parameterized PostgreSQL Queries

Status: **Stage A complete**

Time: **2026-08-06 02:11–02:34 IST (23m)**

## Goal

Learn how to:

- separate SQL structure from runtime values;
- use positional parameters such as `$1`, `$2`, and `$3`;
- test parameterized statements in `psql` with `PREPARE` and `EXECUTE`;
- keep prepared-statement exercises rerunnable with `DEALLOCATE`.

This is Stage A of Checkpoint 17. After it works, Stage B will introduce SQLC
query annotations and a separate application query file.

## Why Values Must Stay Separate from SQL

Unsafe application code builds query text by joining strings:

```text
"SELECT ... WHERE email = '" + userInput + "'"
```

That mixes untrusted data with the SQL program. Quotes or SQL syntax inside
the input can change what the statement means, causing SQL injection.

A parameterized query keeps the structure fixed:

```sql
SELECT id, name, email
FROM customers
WHERE email = $1;
```

The application sends the query and value separately:

```text
SQL structure → SELECT ... WHERE email = $1
value         → asha@example.com
```

PostgreSQL treats the bound value as data, not executable SQL syntax. The
driver also encodes the value, so application code does not quote it manually.

Parameters represent values. They cannot replace identifiers such as table
names, column names, or SQL keywords.

## Positional Parameters

PostgreSQL numbers parameters by position:

```sql
UPDATE order_items
SET quantity = $3
WHERE order_id = $1
  AND product_id = $2;
```

The caller must use the same order:

```text
$1 → order ID
$2 → product ID
$3 → new quantity
```

## Why `$1` Does Not Run Directly in `psql`

This statement contains an unbound parameter:

```sql
SELECT id, name, email
FROM customers
WHERE email = $1;
```

Application drivers bind `$1` when they execute the query. In this raw-SQL
lesson, use PostgreSQL's `PREPARE` command to declare the parameter type:

```sql
PREPARE get_book_by_isbn (TEXT) AS
SELECT id, title, isbn
FROM books
WHERE isbn = $1;
```

Then supply a value with `EXECUTE`:

```sql
EXECUTE get_book_by_isbn('978-1');
```

Read the syntax as:

```text
PREPARE statement_name (parameter types) AS parameterized_statement;
EXECUTE statement_name(actual values);
```

The declared parameter types correspond positionally:

```sql
PREPARE change_item (INTEGER, INTEGER, INTEGER) AS
--                     $1       $2       $3
UPDATE ...;
```

## Prepared Statements Live in the Session

A prepared statement remains available for the current database session. If
you run the same file again, its name would already exist.

Clear session-local prepared statements at the beginning of `main.sql`:

```sql
DEALLOCATE ALL;
```

This makes two consecutive `\i main.sql` runs safe.

`PREPARE`, `EXECUTE`, and `DEALLOCATE` form a testing harness for this lesson.
A production SQLC query file will contain the parameterized statement itself,
not these wrappers.

## Writes Can Return Changed Rows

Use `RETURNING` when application code needs values from an inserted, updated,
or deleted row:

```sql
UPDATE books
SET title = $2
WHERE id = $1
RETURNING id, title;
```

Prefer explicit columns over `RETURNING *`. Explicit columns make the result
contract visible and stable when a table later gains unrelated columns.

## Your Exercise

### Restore the small dataset

In `main.sql`:

1. Keep the Lesson 15 schema, customer-order index, constraints, and original
   seed rows.
2. Remove Lesson 16's generated customers/orders, both `ANALYZE` commands, and
   both `EXPLAIN` statements.
3. Add `DEALLOCATE ALL;` immediately after
   `SET client_min_messages TO WARNING;`.

### Prepare and execute three statements

After the original seed inserts, implement these contracts in order.

#### 1. Get a customer by email

- Prepared name: `get_customer_by_email`
- Parameter types: one `TEXT`
- Return `id`, `name`, and `email` from `customers`.
- Filter `email` using `$1`.
- Execute with `'asha@example.com'`.

#### 2. List orders for a customer

- Prepared name: `list_orders_by_customer`
- Parameter types: one `INTEGER`
- Start from `orders AS o` and join `customers AS c`.
- Return `o.id AS order_id` and `c.email AS customer_email`.
- Filter `o.customer_id` using `$1` and order by `o.id`.
- Execute with customer ID `1`.

#### 3. Update one order-item quantity

- Prepared name: `update_order_item_quantity`
- Parameter types: three `INTEGER` values.
- Treat `$1` as order ID, `$2` as product ID, and `$3` as new quantity.
- Update the matching `order_items` row.
- Return exactly `order_id`, `product_id`, and `quantity`.
- Execute with `(1, 2, 3)`.

Do not concatenate values into SQL. Leave `invalid.sql` unchanged.

## Expected Output

```text
id|name|email
1|Asha|asha@example.com
order_id|customer_email
1|asha@example.com
order_id|product_id|quantity
1|2|3
```

## Run and Verify

Run twice in the same `psql` session:

```text
\i main.sql
\i main.sql
```

Both runs must exactly match the expected output. `DEALLOCATE ALL` must prevent
prepared-statement name collisions.

## Acceptance Criteria

- The small Lesson 15 dataset and index are restored.
- No Lesson 16 bulk data or plan statements remain.
- Repeated execution is safe in one session.
- All runtime values use positional parameters.
- All parameter types are declared explicitly.
- All three statements are executed with the fixed inputs.
- The update uses explicit `RETURNING` columns.
- Output matches on two consecutive runs.
- `invalid.sql` remains unchanged.

## Official Reference

- [PostgreSQL `PREPARE`](https://www.postgresql.org/docs/current/sql-prepare.html)
- [PostgreSQL `EXECUTE`](https://www.postgresql.org/docs/current/sql-execute.html)
- [PostgreSQL `DEALLOCATE`](https://www.postgresql.org/docs/current/sql-deallocate.html)

## Stop Here

Say `done` when both runs match. Do not start SQLC annotations yet; that is
Stage B of this same checkpoint.
