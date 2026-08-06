# Checkpoint 18C: Add and Interpret an Index

Status: **Complete**

Started: **2026-08-06 15:34 IST**

Completed: **2026-08-06 16:37 IST**

Wall time: **1h 03m**

## Goal

Choose one useful index for the bookstore workload, prove that PostgreSQL
created it, and correctly interpret the plan chosen for the current tiny table.

## Two Different Questions

These checks answer different questions:

```text
pg_indexes  → does the intended index exist?
EXPLAIN     → which access path did the planner choose for this query now?
```

An index can exist while PostgreSQL still chooses a sequential scan. With only
two orders, scanning the table can cost less than navigating an index and then
fetching table rows. That does not make the index definition incorrect; a real
order-history table is expected to grow.

## Choose the Access Path

A common API operation is:

```text
list every order belonging to one customer
```

Its filtering shape is:

```sql
SELECT id, customer_id, status
FROM orders
WHERE customer_id = 2;
```

The foreign key on `orders.customer_id` protects the relationship, but
PostgreSQL does not automatically create an index on the child-side foreign-key
column. Create that access path explicitly:

```sql
CREATE INDEX idx_orders_customer_id
ON orders (customer_id);
```

Do not add indexes for `orders.id` or `customers.email`: their `PRIMARY KEY`
and `UNIQUE` constraints already created indexes.

## Prove the Index Definition

PostgreSQL's `pg_indexes` view describes indexes:

```sql
SELECT indexname, indexdef
FROM pg_indexes
WHERE schemaname = 'public'
  AND tablename = 'orders'
  AND indexname = 'idx_orders_customer_id';
```

This proves that the access path exists. It does not prove the planner used it.

## Inspect the Current Plan

Refresh statistics after creating the index:

```sql
ANALYZE orders;
```

Then place the exact customer lookup under:

```sql
EXPLAIN (COSTS OFF)
SELECT ...;
```

Do not use `EXPLAIN ANALYZE` or change planner settings. This stage tests
whether you can accept the cheapest plan for the current data instead of trying
to force an index scan.

## Your Exercise

Keep the Stage A table definitions, constraints, and fixed inserts unchanged.
Remove both Stage B transaction demonstrations and their verification queries.

After the fixed inserts:

1. Create exactly one non-unique index named `idx_orders_customer_id` on
   `orders(customer_id)`.
2. Run `ANALYZE orders`.
3. Run the exact `pg_indexes` query taught above.
4. Use `EXPLAIN (COSTS OFF)` on this exact query:

```sql
SELECT id, customer_id, status
FROM orders
WHERE customer_id = 2;
```

Stop after the plan. Do not add bulk rows, prepared statements, SQLC
annotations, or planner settings.

## Expected Output

Running the whole file must print exactly:

```text
indexname|indexdef
idx_orders_customer_id|CREATE INDEX idx_orders_customer_id ON public.orders USING btree (customer_id)
QUERY PLAN
Seq Scan on orders
  Filter: (customer_id = 2)
```

The sequential scan is expected because the fixed table has only two rows. The
catalog row proves the index is available; the plan proves PostgreSQL still
estimated a table scan as cheaper for this particular dataset.

## Verify

Run the deterministic `psql` command used in Stage B twice. Both complete runs
must print the exact output above.

Then say `done`.

## Acceptance Criteria

- Stage A schema, constraints, and fixed seed rows remain unchanged.
- Stage B transaction demonstrations and result queries are removed.
- Exactly one new explicit index is created.
- It is non-unique and targets `orders(customer_id)`.
- No redundant primary-key or unique-column indexes are added.
- Statistics are refreshed before `EXPLAIN`.
- The catalog output proves the intended index exists.
- Plain `EXPLAIN (COSTS OFF)` reports the planner's unforced choice.
- The complete file is rerunnable and prints the expected output twice.
