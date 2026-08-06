# Checkpoint 14: Make Changes Atomic with Transactions

Status: **Complete**

## Goal

Learn how to:

- understand PostgreSQL's default autocommit behavior;
- group multiple SQL statements into one transaction;
- make all grouped changes permanent with `COMMIT`;
- discard all grouped changes with `ROLLBACK`;
- understand what PostgreSQL does when a statement fails inside a transaction.

## Why Transactions Exist

Many business operations require more than one SQL statement. A bank transfer,
for example, has at least two changes:

```text
subtract money from one account
add money to another account
```

If the first statement succeeds and the second fails, the database must not
keep only half of the transfer.

A transaction lets the database treat several statements as one unit:

```text
all changes become permanent
              or
none of the changes become permanent
```

This property is **atomicity**: the operation is treated as indivisible.

## PostgreSQL Normally Uses Autocommit

Without an explicit transaction, each successful statement is committed by
itself:

```sql
UPDATE accounts
SET balance_paise = balance_paise - 1000
WHERE id = 1;

UPDATE accounts
SET balance_paise = balance_paise + 1000
WHERE id = 2;
```

PostgreSQL treats those as two independent transactions. If the second
statement fails, the first one is already permanent.

Autocommit is convenient for independent statements. It is unsafe when
multiple statements together represent one business operation.

## The Transaction Boundary

Use `BEGIN` to open a transaction and `COMMIT` to make all its changes
permanent:

```sql
BEGIN;

UPDATE accounts
SET balance_paise = balance_paise - 1000
WHERE id = 1;

UPDATE accounts
SET balance_paise = balance_paise + 1000
WHERE id = 2;

COMMIT;
```

Read the commands as boundaries:

```text
BEGIN    → start collecting changes in this transaction
COMMIT   → permanently accept all collected changes
ROLLBACK → discard all collected changes
```

`BEGIN` is PostgreSQL's shorter spelling of `START TRANSACTION`. They open the
same kind of transaction. Use `BEGIN` in this lesson.

## `ROLLBACK` Discards the Whole Transaction

Replace `COMMIT` with `ROLLBACK` when the work must be abandoned:

```sql
BEGIN;

-- one or more changes

ROLLBACK;
```

`ROLLBACK` is not an “undo the previous statement” command. It ends the
current transaction and discards every uncommitted change made since `BEGIN`.

## Changes Are Visible Inside the Transaction

Statements later in the same transaction see earlier uncommitted changes. A
`SELECT` before `ROLLBACK` sees the changed value; a `SELECT` afterward sees
the original value again.

Other database sessions normally cannot see these uncommitted changes. That
is part of transaction **isolation**; this checkpoint focuses on atomicity.

## What Happens When a Statement Fails?

If a statement violates a constraint or otherwise fails, PostgreSQL marks the
whole transaction as failed:

```sql
BEGIN;
-- first valid change
-- second change fails
```

After the error, ordinary statements in that transaction are rejected with a
message shaped like:

```text
ERROR: current transaction is aborted, commands ignored until end of transaction block
```

Run `ROLLBACK;` to end the failed transaction. The first change is discarded
too; PostgreSQL will not silently commit the successful half.

This is the normal application control flow:

```text
BEGIN
  ↓
run every required statement
  ↓
any statement failed? ── yes ──→ ROLLBACK
  │
  no
  ↓
COMMIT
```

Go's transaction API later follows this same control flow.

## Transactions and Constraints Work Together

A transaction does not replace constraints:

- constraints decide whether each database state is valid;
- a transaction decides whether a group of changes is accepted together.

Constraints validate the rows; the transaction prevents a partial operation
when one statement fails.

## Your Exercise

Keep the complete Lesson 13 schema and seed data. Replace only its final
four-table report query with the transaction exercise below.

You will change the quantities of the two products in order `1` as one unit.
The starting values are:

```text
Raagi Malt|2
Sprout Salad|1
```

### Part A: Change and roll back

1. Open a transaction.
2. Update the Raagi Malt order item from quantity `2` to `4`.
3. Update the Sprout Salad order item from quantity `1` to `2`.
4. Roll back the transaction.
5. Run one result query showing the two unchanged quantities.

Identify each order item using both `order_id` and `product_id`. Return:

```text
'after_rollback' AS phase, p.name AS product_name, oi.quantity
```

Join `order_items` to `products` and restrict the result to order `1`. Order by
product ID.

### Part B: Change and commit

1. Open a new transaction.
2. Perform the same two quantity updates.
3. Commit the transaction.
4. Run the same result query, but return `'after_commit' AS phase`.

Do not change `unit_price_paise`. Leave `invalid.sql` unchanged.

## Expected Output

```text
phase|product_name|quantity
after_rollback|Raagi Malt|2
after_rollback|Sprout Salad|1
phase|product_name|quantity
after_commit|Raagi Malt|4
after_commit|Sprout Salad|2
```

The first result proves that `ROLLBACK` discarded both updates. The second
proves that `COMMIT` preserved both updates.

## Run and Verify

From `databases`, enter `psql`:

```bash
docker compose exec postgres \
  psql --username course_user --dbname sql_course
```

If needed, configure the deterministic display used by the expected output:

```text
\set QUIET on
\pset format unaligned
\pset fieldsep '|'
\pset tuples_only off
\pset footer off
```

Run the file twice:

```text
\i main.sql
\i main.sql
```

Both runs must produce the exact expected output. The schema recreation and
seed data at the beginning of `main.sql` reset the starting quantities.

## Acceptance Criteria

- The Lesson 13 schema, constraints, and seed rows remain unchanged.
- Part A uses one `BEGIN` and ends with `ROLLBACK`.
- Both Part A updates occur before the rollback.
- The first query proves that neither Part A update persisted.
- Part B opens a new transaction and ends with `COMMIT`.
- Both Part B updates occur before the commit.
- Each update targets one row using both order ID and product ID.
- Both result queries use a join and deterministic product-ID ordering.
- Output exactly matches on two consecutive runs.
- `invalid.sql` remains unchanged.

## Stop Here

Say `done` when both runs match. Do not start indexes yet.
