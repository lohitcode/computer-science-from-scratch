# Checkpoint 16: Understand Query Execution with `EXPLAIN`

Status: **Complete**

## Goal

Learn how to:

- separate declarative SQL from its physical execution plan;
- inspect a plan with `EXPLAIN`;
- distinguish a sequential scan from an index scan;
- give PostgreSQL useful statistics with `ANALYZE`;
- understand why an existing index may not be selected;
- distinguish `EXPLAIN` from `EXPLAIN ANALYZE`.

## SQL Says What, the Planner Chooses How

This query describes the result you want:

```sql
SELECT id, customer_id
FROM orders
WHERE customer_id = 1;
```

It does not command PostgreSQL to use an index. PostgreSQL's planner compares
possible execution strategies and chooses the one it estimates will cost the
least.

Possible strategies include:

```text
scan every table row and test the condition
follow an index to matching table rows
combine several indexes
```

This separation is central to relational databases:

```text
SQL query      → logical request: what result is needed?
query plan     → physical strategy: how will PostgreSQL produce it?
```

## Inspect the Planned Strategy

Prefix a statement with `EXPLAIN`:

```sql
EXPLAIN
SELECT id, customer_id
FROM orders
WHERE customer_id = 1;
```

Plain `EXPLAIN` plans the statement but does not execute the `SELECT`.

The normal output includes estimates such as costs, rows, and row width. Those
numbers may vary with statistics and PostgreSQL settings. This lesson hides
them to produce a stable learning output:

```sql
EXPLAIN (COSTS OFF)
SELECT id, customer_id
FROM orders
WHERE customer_id = 1;
```

`COSTS OFF` changes only the displayed plan details. It does not change the
planner's decision.

## Sequential Scan

Without a useful index, the plan can be:

```text
Seq Scan on orders
  Filter: (customer_id = 1)
```

Read it as:

```text
Seq Scan → visit rows from the orders table sequentially
Filter   → keep only rows satisfying customer_id = 1
```

A sequential scan is not automatically bad. It is often cheapest when:

- the table is small;
- the query needs a large percentage of its rows;
- no useful index exists.

## Index Scan

With a selective condition and the Lesson 15 index, the plan can become:

```text
Index Scan using idx_orders_customer_id on orders
  Index Cond: (customer_id = 1)
```

Read it as:

```text
Index Scan → navigate the index to find matching entries
Index Cond → condition used to search the index
```

The index narrows the search before PostgreSQL fetches the matching table
rows.

## Bitmap Index Scan and Bitmap Heap Scan

PostgreSQL has another index-based strategy that commonly appears between a
sequential scan and a plain index scan:

```text
Bitmap Heap Scan on orders
  Recheck Cond: (customer_id = 1)
  -> Bitmap Index Scan on idx_orders_customer_id
       Index Cond: (customer_id = 1)
```

This is one plan with two nodes:

```text
Bitmap Index Scan → find matching index entries and build a bitmap of table pages
Bitmap Heap Scan  → visit those table pages in a convenient physical order
Recheck Cond      → verify the condition when reading the table rows
```

A plain index scan follows index entries to table rows one at a time. A bitmap
plan first collects locations and then groups the table-page visits. That can
be cheaper when PostgreSQL expects more than a tiny number of matches but far
fewer than the whole table.

If statistics are stale or missing after a bulk insert, the planner may
misestimate how selective `customer_id = 1` is and choose this bitmap plan.
After `ANALYZE orders`, it learns that only one of 10,002 orders matches and a
plain index scan becomes cheaper.

Both `Bitmap Index Scan` and `Index Scan` mean the index is being used. The
difference is how PostgreSQL retrieves the matching table rows.

## Why the Two-Row Table May Ignore the Index

Your Lesson 15 table has only two orders. Reading two nearby table rows is
likely cheaper than navigating a separate index and then visiting the table.

Therefore, “I created an index” does not imply “PostgreSQL must use it.” The
planner chooses based on estimated work.

This lesson adds enough data and makes `customer_id = 1` selective:

```text
total orders              → 10,002
orders for customer 1     → 1
```

Finding one row out of 10,002 is a realistic index-shaped access pattern.

## Generate Repeatable Practice Data

`generate_series(start, stop)` is a PostgreSQL set-returning function. It
produces one row for every integer in the inclusive range:

```sql
SELECT n
FROM generate_series(3, 6) AS n;
```

Output:

```text
n
3
4
5
6
```

It can feed an `INSERT ... SELECT`:

```sql
INSERT INTO customers (name, email)
SELECT
    'Customer ' || n,
    'customer' || n || '@example.com'
FROM generate_series(3, 10002) AS n;
```

`||` concatenates text in PostgreSQL. The generated values are unique because
`n` changes for each row.

Similarly, create one order for each new customer:

```sql
INSERT INTO orders (customer_id)
SELECT n
FROM generate_series(3, 10002) AS n;
```

Customers `1` and `2` and their orders already came from the fixed seed data.
The new rows extend both sets through ID `10002`.

## Give the Planner Statistics with `ANALYZE`

The planner estimates costs using statistics about table size and value
distribution. Refresh the statistics after bulk-loading practice data:

```sql
ANALYZE orders;
```

This `ANALYZE` command does not return application rows or change their
values. It samples the table and updates planner statistics.

## Do Not Confuse Two Different Uses of `ANALYZE`

These commands have different effects:

```sql
ANALYZE orders;
```

```text
collect planner statistics for orders
```

```sql
EXPLAIN ANALYZE
SELECT ...;
```

```text
execute the statement and report estimates plus actual measurements
```

Plain `EXPLAIN` does not run the described statement. `EXPLAIN ANALYZE` does.
That distinction is especially important for `INSERT`, `UPDATE`, and `DELETE`:
`EXPLAIN ANALYZE` would actually perform the data change unless you protect it
with a transaction and roll it back.

This exercise uses plain `EXPLAIN (COSTS OFF)` for deterministic output.

## Your Exercise

Keep the Lesson 15 schema, constraints, and original seed rows. Change only
the index placement and replace the two Lesson 15 result queries.

1. Remove the Lesson 15 `CREATE INDEX` from its current location. Do not create
   the index yet.
2. After all original seed inserts, insert customers numbered `3` through
   `10002` using the exact `INSERT ... SELECT` and `generate_series` pattern
   taught above.
3. Insert one order per generated customer using the second taught statement.
4. Refresh statistics for `orders`.
5. Run this exact query through `EXPLAIN (COSTS OFF)`:

```sql
SELECT id, customer_id
FROM orders
WHERE customer_id = 1;
```

6. Create `idx_orders_customer_id` on `orders(customer_id)` using the Lesson 15
   syntax.
7. Run `ANALYZE orders` again. The table data has not changed, so this second
   call is not normally necessary for this simple index; it is required here
   to keep the learning output deterministic and to reinforce that current
   statistics influence plan selection.
8. Run the exact same query through `EXPLAIN (COSTS OFF)` again.

Do not use `EXPLAIN ANALYZE`, planner-enabling settings such as
`enable_seqscan`, or `IF NOT EXISTS`. Leave `invalid.sql` unchanged.

## Expected Output

```text
QUERY PLAN
Seq Scan on orders
  Filter: (customer_id = 1)
QUERY PLAN
Index Scan using idx_orders_customer_id on orders
  Index Cond: (customer_id = 1)
```

The SQL query is identical in both cases. Only the available access paths
change.

## Run and Verify

From `databases`, run the file twice:

```text
\i main.sql
\i main.sql
```

Both executions must reproduce the two plan shapes exactly.

## Acceptance Criteria

- The Lesson 15 tables, constraints, and original seed rows remain unchanged.
- Exactly 10,000 additional customers and orders are generated.
- The first plan is captured before creating the customer-order index.
- `ANALYZE orders` runs after the bulk insert.
- The first plan contains `Seq Scan` and `Filter`.
- The index is then created with the exact Lesson 15 name and column.
- The second plan uses the identical `SELECT` statement.
- The second plan contains `Index Scan` and `Index Cond`.
- No planner behavior is forced through configuration settings.
- Output matches on two consecutive runs.
- `invalid.sql` remains unchanged.

## Official References

- [`EXPLAIN`](https://www.postgresql.org/docs/current/sql-explain.html)
- [Using `EXPLAIN`](https://www.postgresql.org/docs/current/using-explain.html)
- [`ANALYZE`](https://www.postgresql.org/docs/current/sql-analyze.html)
- [Planner statistics](https://www.postgresql.org/docs/current/planner-stats-details.html)

## Stop Here

Say `done` when both runs match. Do not start application query shapes yet.
