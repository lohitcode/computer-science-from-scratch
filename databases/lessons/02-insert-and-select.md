# Checkpoint 02: Insert and Select Rows

## Goal

In this checkpoint:

1. insert rows into `products`;
2. retrieve every column;
3. retrieve one specific column.

Do not add prices, constraints, or filters yet.

## Problem Contract

### Starting state

`main.sql` already drops and recreates:

```text
products(id, name)
```

### Required work

After `CREATE TABLE`, your final file must contain all four blocks:

1. One individual `INSERT` that adds `Raagi Malt`.
2. A second, multi-row `INSERT` that adds `Fruit Juice` and `Sprout Salad`.
3. `SELECT * FROM products;`
4. `SELECT name FROM products;`

Both insert styles are required. Do not replace the individual insert with the
multi-row insert or the multi-row insert with the individual insert.

Your inserts must omit `id`. Since the script first recreates the table, SQLite
will assign IDs `1`, `2`, and `3` in insertion order.

### Fixed input

| Insert style | `name` |
|---|---|
| Individual insert | `Raagi Malt` |
| Multi-row insert, first row | `Fruit Juice` |
| Multi-row insert, second row | `Sprout Salad` |

Use these exact spellings and capitalization. SQL text values must use single
quotes.

### Expected output

SQLite output formatting depends on its current mode. Set a known mode before
running the file so your terminal can be compared with this transcript:

```text
sqlite> .mode list
sqlite> .headers off
sqlite> .read main.sql
1|Raagi Malt
2|Fruit Juice
3|Sprout Salad
Raagi Malt
Fruit Juice
Sprout Salad
sqlite>
```

The first three lines are produced by `SELECT *`. The final three lines are
produced by `SELECT name`.

The three logical rows must match even if SQLite displays them in a different
order. SQL does not guarantee row order without an explicit ordering clause;
ordering is taught in checkpoint 05.

### Acceptance criteria

- The script runs without an SQL error.
- The table contains exactly three products.
- The names exactly match the fixed input.
- SQLite assigns IDs `1`, `2`, and `3` because the inserts omit `id`.
- The first query displays both `id` and `name`.
- The second query displays only `name`.
- Running the complete script twice does not duplicate the rows.

## Schema Versus Rows

Checkpoint 01 created the shape:

```text
products
├── id
└── name
```

The table exists, but it has no rows until an `INSERT` stores data.

```text
CREATE TABLE → define the structure
INSERT       → store rows
SELECT       → retrieve rows
```

## Insert One Row

Here is an example using the `books` table:

```sql
INSERT INTO books (title)
VALUES ('The Go Programming Language');
```

Read it as:

```text
INSERT INTO books   choose the destination table
(title)             choose the destination column
VALUES (...)        provide the value for that column
```

Text values use single quotes. The statement ends with a semicolon.

The example omits `id`. With SQLite's `INTEGER PRIMARY KEY`, SQLite assigns the
ID automatically.

## Insert Several Rows

One statement can insert multiple rows:

```sql
INSERT INTO books (title)
VALUES
    ('Designing Data-Intensive Applications'),
    ('The C Programming Language');
```

Each parenthesized value group becomes one row.

## Select Rows

Select every column:

```sql
SELECT *
FROM books;
```

`*` means every column.

Select only one column:

```sql
SELECT title
FROM books;
```

SQL may span multiple lines. SQLite executes the statement when it reaches the
semicolon.

## Required File Order

Organize `main.sql` in this order:

```text
drop old table
create new table
individual insert: Raagi Malt
multi-row insert: Fruit Juice and Sprout Salad
select every column
select only name
```

SQLite cannot insert into a table before that table exists.

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
```

You should see:

- the first query displaying `id` and `name`;
- exactly the three fixed product rows;
- the second query displaying only `name`;
- automatically assigned IDs `1`, `2`, and `3`.

Run `.read main.sql` again. Because your script drops and rebuilds `products`,
the row count should remain the same instead of duplicating.

Inspect manually if needed:

```text
.schema products
```

Exit with:

```text
.quit
```

## Check Your Understanding

1. What is the difference between `CREATE TABLE`, `INSERT`, and `SELECT`?
2. Why must the column list correspond to the values?
3. Why are product names surrounded by single quotes?
4. Why can you omit `id` in these inserts?
5. Why does running the complete file again not duplicate the rows?
6. What does `*` mean in `SELECT *`?

## Stop Here

Send me:

1. your updated `main.sql`;
2. the output from `.read main.sql`.

Ask questions as soon as something is unclear. After this works, checkpoint 03
will add constraints that prevent invalid product data.
