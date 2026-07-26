# Checkpoint 04: Filter Rows

## Goal

Use `WHERE` to retrieve only rows that satisfy fixed conditions.

Do not sort, limit, update, or delete rows yet.

## Problem Contract

### Starting state

Keep the checkpoint 03 schema and these exact rows:

| `id` | `name` | `price_paise` | `available` |
|---:|---|---:|---:|
| 1 | Raagi Malt | 5000 | 1 |
| 2 | Fruit Juice | 8000 | 1 |
| 3 | Sprout Salad | 6500 | 0 |

Do not change the schema or inserts. Replace the final `SELECT *` in `main.sql`
with the five queries below.

### Required queries

Every query must select only `name`.

1. Products where `available` equals `1`.
2. Products where `price_paise` is greater than or equal to `6000`.
3. Products where `available` equals `1` **and** `price_paise` is less than
   `6000`.
4. Products whose name is `Fruit Juice` **or** `Sprout Salad`.
5. Products where it is **not true** that `available` equals `1`.

Use `AND`, `OR`, and `NOT` in queries 3–5. For query 5, use parentheses to make
the negated condition explicit.

### Expected output

Use:

```text
sqlite> .mode list
sqlite> .headers on
sqlite> .read main.sql
name
Raagi Malt
Fruit Juice
name
Fruit Juice
Sprout Salad
name
Raagi Malt
name
Fruit Juice
Sprout Salad
name
Sprout Salad
sqlite>
```

Each `name` header begins the output of the next query. The logical rows must
match this transcript. SQL does not guarantee row order without `ORDER BY`, so
the order within a result is not part of this checkpoint.

### Acceptance criteria

- The schema and three inserted rows are unchanged.
- `main.sql` contains the five required queries in the listed order.
- Every query returns only the `name` column.
- The five logical result sets match the expected output.
- Queries 3, 4, and 5 use `AND`, `OR`, and `NOT`, respectively.
- Running the complete script twice produces the same database state and
  results.

## How `WHERE` Works

Without a filter:

```sql
SELECT title
FROM books;
```

Every book is eligible for the result.

With a filter:

```sql
SELECT title
FROM books
WHERE page_count >= 300;
```

SQLite checks the condition for each row and keeps rows where it evaluates to
true.

```text
FROM books               choose the source rows
WHERE page_count >= 300  keep matching rows
SELECT title             return this column
```

SQL is written as `SELECT`, `FROM`, `WHERE`, even though the source-and-filter
mental model is useful when reading it.

## Comparison Operators

| Operator | Meaning |
|---|---|
| `=` | Equal |
| `!=` or `<>` | Not equal |
| `<` | Less than |
| `<=` | Less than or equal |
| `>` | Greater than |
| `>=` | Greater than or equal |

SQL equality uses one equals sign:

```sql
WHERE in_stock = 1
```

It does not use Go's `==`.

## Combine Conditions

`AND` requires both conditions:

```sql
SELECT title
FROM books
WHERE in_stock = 1 AND page_count < 500;
```

`OR` requires at least one condition:

```sql
SELECT title
FROM books
WHERE author = 'Author A' OR author = 'Author B';
```

`NOT` reverses a condition:

```sql
SELECT title
FROM books
WHERE NOT (in_stock = 1);
```

Parentheses make it clear which complete condition `NOT` reverses.

## Run and Verify

From the `databases` directory:

```bash
sqlite3 practice/sql-course.db
```

Inside SQLite:

```text
.mode list
.headers on
.read main.sql
```

Compare each result set with the expected transcript before saying `done`.
Preserve `invalid.sql`; it is a completed checkpoint 03 test file and is not
executed for this checkpoint.

## Stop Here

Send me:

1. your updated `main.sql`;
2. the complete output from `.read main.sql`.

Ask questions as soon as a condition is unclear. Do not begin ordering or
pagination until this checkpoint has been reviewed.
