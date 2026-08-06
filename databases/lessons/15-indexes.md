# Checkpoint 15: Make Reads Faster with an Index

Status: **Complete**

## Goal

Learn how to:

- understand the problem an index solves;
- create a PostgreSQL B-tree index;
- recognize indexes already created by constraints;
- choose a useful foreign-key index without creating a redundant one;
- understand why indexes improve reads but add write and storage costs.

This lesson creates an index. Lesson 16 will use `EXPLAIN` to observe whether
the query planner chooses it.

## Why an Index Exists

Without an index, PostgreSQL may need to inspect every row to find matches:

```text
row 1 → not customer 42
row 2 → not customer 42
row 3 → customer 42
...
row 1,000,000 → not customer 42
```

That is a sequential scan. Its work grows with the table.

An index is a separate data structure containing indexed values and pointers
to table rows. It is similar to a book index: find an ordered entry first,
then follow it to the full information.

PostgreSQL uses a B-tree when `CREATE INDEX` does not specify another index
type. A B-tree keeps keys ordered in a balanced, multi-level tree, making it
useful for equality, ranges, and ordered retrieval.

## Create a Basic Index

Suppose an application frequently loads orders for one customer:

```sql
SELECT id, customer_id
FROM orders
WHERE customer_id = 42;
```

Create an index whose leading column matches that search condition:

```sql
CREATE INDEX idx_orders_customer_id
ON orders (customer_id);
```

Read the syntax as:

```text
CREATE INDEX index_name
ON table_name (indexed_column);
```

`idx_orders_customer_id` is an ordinary explicit name. A useful convention is:

```text
idx_<table>_<column-or-purpose>
```

The name does not affect performance, but a descriptive name helps migrations
and error investigation.

To remove an index while keeping its table:

```sql
DROP INDEX idx_orders_customer_id;
```

Dropping a table automatically removes indexes belonging to that table, so
your existing child-first table recreation remains rerunnable.

## Constraints Already Created Some Indexes

Do not add an index merely because a column looks important. PostgreSQL
automatically creates unique B-tree indexes for primary-key and unique
constraints.

Your current schema therefore already has index support for examples such as:

```text
products.id                      ← PRIMARY KEY
products.name                    ← UNIQUE
customers.email                  ← UNIQUE
order_items.id                   ← PRIMARY KEY
(order_items.order_id,
 order_items.product_id)         ← UNIQUE pair
```

Creating another ordinary index on exactly the same column or column sequence
would usually be redundant: it consumes storage and must also be maintained
on writes without adding a new useful access path.

## A Foreign Key Does Not Automatically Index the Child Column

This constraint protects correctness:

```sql
customer_id INTEGER NOT NULL REFERENCES customers(id)
```

The referenced parent key, `customers.id`, is indexed because it is a primary
key. PostgreSQL does **not** automatically create an index on the referencing
child column, `orders.customer_id`.

That choice is intentional. Not every foreign key is queried often, and the
best useful index might contain multiple columns. Schema designers decide
which child-side access paths the application needs.

For your schema, customer order history is a realistic query:

```sql
WHERE orders.customer_id = ?
```

Therefore, `orders(customer_id)` is a reasonable index.

## Composite Index Order Matters

Your unique constraint created a composite index ordered like this:

```text
(order_id, product_id)
```

A multicolumn B-tree is most efficient when a query constrains its leading,
leftmost columns:

```sql
WHERE order_id = 1
```

or:

```sql
WHERE order_id = 1 AND product_id = 2
```

It is not generally an efficient substitute for an index beginning with
`product_id` when the query searches only this:

```sql
WHERE product_id = 2
```

Think of a phone book ordered by `(last_name, first_name)`: it is easy to find
everyone with one last name, but not everyone with one first name.

For this checkpoint, do not create another `order_items` index. The lesson's
single target is `orders(customer_id)`.

## Indexes Are Not Free

An index usually trades write cost and storage for faster reads:

```text
SELECT using indexed conditions → can become faster
INSERT                          → must add an index entry
UPDATE indexed column           → must update the index
DELETE                          → must remove an index entry
disk and memory                 → index occupies space
```

Small tables may be faster to scan directly. Even when an index exists,
PostgreSQL's planner decides whether to use it. Creating an index does not
force every matching query through it.

## Inspect Indexes with `pg_indexes`

`pg_indexes` is a PostgreSQL system view describing available indexes. This
query checks one index and reconstructs its definition:

```sql
SELECT indexname, indexdef
FROM pg_indexes
WHERE schemaname = 'public'
  AND tablename = 'orders'
  AND indexname = 'idx_orders_customer_id';
```

Expected shape:

```text
idx_orders_customer_id|CREATE INDEX ... USING btree (customer_id)
```

This proves that the index exists and targets the intended column. It does not
prove that a particular query uses it; that is the purpose of `EXPLAIN` in the
next lesson.

## Your Exercise

Keep the Lesson 14 schema, constraints, and seed data unchanged. Remove the
two transaction demonstrations and their result queries.

1. Create one non-unique index named `idx_orders_customer_id` on
   `orders(customer_id)`.
2. Do not add `IF NOT EXISTS`; recreating the `orders` table already removes
   and recreates its indexes on every run.
3. Add the exact `pg_indexes` inspection query shown above.
4. Add one application-shaped query that returns:

```text
o.id AS order_id, c.email AS customer_email
```

Start from `orders AS o`, join `customers AS c` through their key relationship,
filter with `o.customer_id = 1`, and order by `o.id`.

Leave `invalid.sql` unchanged.

## Expected Output

```text
indexname|indexdef
idx_orders_customer_id|CREATE INDEX idx_orders_customer_id ON public.orders USING btree (customer_id)
order_id|customer_email
1|asha@example.com
```

The small seed table may not benefit from the index yet. The goal here is to
design and create the correct access path; Lesson 16 will examine planner
behavior with enough data to make the tradeoff visible.

## Run and Verify

From `databases`, enter `psql` and run twice:

```text
\i main.sql
\i main.sql
```

Both executions must produce the exact expected output.

You can additionally inspect the table with:

```text
\d orders
```

## Acceptance Criteria

- The Lesson 14 schema, constraints, and seed rows remain unchanged.
- The transaction demonstration is removed.
- Exactly one new explicit index is created.
- It is non-unique and targets `orders(customer_id)`.
- Its name is exactly `idx_orders_customer_id`.
- No redundant explicit indexes are added for primary or unique constraints.
- The catalog query reports the expected index definition.
- The application query uses the indexed column in its `WHERE` condition.
- Both queries have deterministic output and match on two consecutive runs.
- `invalid.sql` remains unchanged.

## Official References

- [PostgreSQL indexes](https://www.postgresql.org/docs/current/indexes.html)
- [`CREATE INDEX`](https://www.postgresql.org/docs/current/sql-createindex.html)
- [Multicolumn indexes](https://www.postgresql.org/docs/current/indexes-multicolumn.html)
- [`pg_indexes`](https://www.postgresql.org/docs/current/view-pg-indexes.html)

## Stop Here

Say `done` when both runs match. Do not start `EXPLAIN` yet.
