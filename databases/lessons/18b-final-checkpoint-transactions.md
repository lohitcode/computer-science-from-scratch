# Checkpoint 18B: Prove Atomic Changes

Status: **Complete**

Started: **2026-08-06 15:12 IST**

Completed: **2026-08-06 15:34 IST**

Wall time: **22m**

## Goal

Use the Stage A bookstore schema to prove that a logical operation containing
multiple writes can be discarded completely or saved completely.

This stage introduces no new transaction syntax. It tests whether you can
choose the transaction boundary and verify the state after `ROLLBACK` and
`COMMIT`.

## Mental Model

An application action can require several SQL statements. For example,
completing a shipment might update both its state and its tracking code:

```sql
BEGIN;

UPDATE shipments
SET status = 'sent'
WHERE id = 7;

UPDATE shipments
SET tracking_code = 'TRACK-7'
WHERE id = 7;

COMMIT;
```

The transaction boundary says these statements form one logical change. Other
sessions must not observe a permanently half-finished result.

Replacing `COMMIT` with `ROLLBACK` discards both updates:

```sql
BEGIN;

UPDATE shipments SET status = 'sent' WHERE id = 7;
UPDATE shipments SET tracking_code = 'TRACK-7' WHERE id = 7;

ROLLBACK;
```

`ROLLBACK` is not an alternative kind of success. It means the attempted unit
of work must leave no permanent effect.

## Your Exercise

Keep all Stage A table definitions and fixed inserts. Remove the Stage A report
at the bottom and replace it with the work below.

### Part 1: Attempt and discard a change

Start a transaction for order `2`.

1. Change that order's status from `pending` to `cancelled`.
2. Change its order item's quantity from `1` to `4`.
3. Roll back the transaction.
4. Query the order and its item to prove both original values remain.

The verification query must return these aliases in this order:

```text
phase, order_id, status, book_id, quantity
```

Produce the constant phase value `after_rollback` with:

```sql
'after_rollback' AS phase
```

### Part 2: Perform and save a change

Start a second transaction for order `2`.

1. Change its status from `pending` to `paid`.
2. Change its order item's quantity from `1` to `2`.
3. Commit the transaction.
4. Run the same joined verification shape using the phase value
   `after_commit`.

Use targeted `WHERE` conditions for every update. Do not rely on current row
order, and do not change the fixed inserts to fake the final result.

Stop after the second verification query. Indexes and application queries come
in the next stage.

## Expected Output

Running the whole file must print exactly:

```text
phase|order_id|status|book_id|quantity
after_rollback|2|pending|3|1
phase|order_id|status|book_id|quantity
after_commit|2|paid|3|2
```

The first row proves that neither attempted write survived the rollback. The
second proves that both committed writes survived together.

## Verify

Run the same deterministic `psql` command from Stage A twice. Both complete
runs must print the exact output above.

Then say `done`.

## Acceptance Criteria

- Stage A schema, constraints, and fixed seed rows remain unchanged.
- The Stage A report is removed so there is no extra output.
- Each logical change has its own explicit transaction.
- The first transaction changes two rows and then rolls back.
- The second transaction changes two rows and then commits.
- Every `UPDATE` is targeted to order `2` or its `(order_id, book_id)` item.
- Joined verification runs only after each transaction ends.
- The complete file is rerunnable and prints the exact expected output twice.
