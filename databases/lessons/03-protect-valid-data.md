# Checkpoint 03: Protect Valid Data

## Goal

Extend `products` so the database rejects invalid names, prices, and
availability values.

Do not add filtering, sorting, updates, or deletes yet.

## Problem Contract

### Starting state

`main.sql` currently creates:

```text
products(id, name)
```

It inserts the three products completed in checkpoint 02.

### Required schema

Change `products` to contain:

| Column | Required definition |
|---|---|
| `id` | Integer primary key |
| `name` | Required, unique text |
| `price_paise` | Required integer that cannot be negative |
| `available` | Required integer, only `0` or `1`, default `1` |

### Fixed valid input

| `name` | `price_paise` | `available` |
|---|---:|---:|
| Raagi Malt | 5000 | Omit this value to test the default |
| Fruit Juice | 8000 | 1 |
| Sprout Salad | 6500 | 0 |

Keep one individual insert for `Raagi Malt` and one multi-row insert for the
other two products. Continue omitting every `id`.

### Required output query

After the inserts, keep only this query:

```sql
SELECT *
FROM products;
```

### Expected output

Use deterministic SQLite formatting:

```text
sqlite> .mode list
sqlite> .headers off
sqlite> .read main.sql
1|Raagi Malt|5000|1
2|Fruit Juice|8000|1
3|Sprout Salad|6500|0
sqlite>
```

The important default behavior is:

```text
Raagi Malt omitted available → SQLite stored 1
```

### Invalid-input checks

Create a second file named `invalid.sql`. Write four separate inserts that
attempt to store:

| Test | Fixed invalid input | Expected result |
|---|---|---|
| Missing name | Omit `name`; use price `1000` | Rejected by `NOT NULL` |
| Negative price | `Broken Price`, `-1`, available `1` | Rejected by `CHECK` |
| Invalid availability | `Broken Availability`, `1000`, available `2` | Rejected by `CHECK` |
| Duplicate name | `Raagi Malt`, `5000`, available `1` | Rejected by `UNIQUE` |

At the end of `invalid.sql`, add:

```sql
SELECT *
FROM products;
```

All four inserts must fail, and the final query must still show exactly the
three valid rows.

SQLite error messages include source line numbers that depend on your file
layout. The line numbers are not tested. The four rejection reasons and final
database state are tested.

### Acceptance criteria

- `main.sql` runs without errors.
- Its output matches the three expected valid rows.
- `available` defaults to `1` for `Raagi Malt`.
- `invalid.sql` produces four constraint errors.
- No invalid row is stored.
- The final table still contains exactly three rows.
- Running `main.sql` again resets the database to the same valid state.

## Why Constraints Belong in the Database

Application code can contain bugs, and more than one application may write to
the same database. Schema constraints protect the data regardless of which
caller sends it.

```text
application validation → friendly error for the user
database constraint    → final protection for stored data
```

Production systems commonly use both.

## Constraint Vocabulary

Here is an example using a different table:

```sql
CREATE TABLE books (
    id INTEGER PRIMARY KEY,
    isbn TEXT NOT NULL UNIQUE,
    page_count INTEGER NOT NULL CHECK (page_count > 0),
    in_stock INTEGER NOT NULL DEFAULT 1 CHECK (in_stock IN (0, 1))
);
```

Read the new rules as:

```text
NOT NULL   a value must be supplied
UNIQUE     another row cannot contain the same value
DEFAULT 1  use 1 when the insert omits this column
CHECK      accept the value only when its expression is true
IN (0, 1)  value must be one of these choices
```

A default is used only when the column is omitted. It does not replace an
explicit invalid value.

## Keep Valid and Invalid SQL Separate

Use:

```text
main.sql      rebuilds a known-valid database
invalid.sql   proves that forbidden rows are rejected
```

This separation keeps your normal script successful while preserving negative
tests as source code.

## Run and Verify

From the `databases` directory:

```bash
sqlite3 practice/sql-course.db
```

Inside SQLite:

```text
.mode list
.headers off
.read main.sql
.bail off
.read invalid.sql
```

`.bail off` tells the CLI to continue reading the test file after an expected
error. Otherwise, the first rejected insert could prevent later checks from
running.

## Stop Here

Send me:

1. `main.sql`;
2. `invalid.sql`;
3. the complete output from both `.read` commands.

Ask questions immediately if any constraint is unclear. Do not start filtering
until this checkpoint has been reviewed.
