# Checkpoint 05: Sort and Limit Results

Status: **Complete**

## Goal

Learn how to:

- guarantee the order of query results with `ORDER BY`;
- sort from low to high with `ASC`;
- sort from high to low with `DESC`;
- break ties with more than one ordering column;
- return only part of a result with `LIMIT`;
- skip rows with `OFFSET`.

The examples below use a `books` table. Your exercise still uses the
`products` table in `main.sql`.

## Example Data

Imagine that `books` contains these rows:

| `id` | `title` | `price_paise` | `available` |
|---:|---|---:|---|
| 1 | Go Basics | 50000 | `TRUE` |
| 2 | SQL Basics | 30000 | `TRUE` |
| 3 | Networks | 50000 | `FALSE` |
| 4 | Linux | 70000 | `TRUE` |

## 1. Why `ORDER BY` Is Necessary

This query does **not** guarantee which row PostgreSQL returns first:

```sql
SELECT title, price_paise
FROM books;
```

A table has no promised display order. Rows may appear in insertion order
today and a different order after an index, update, or query-plan change.

Whenever order matters, state it explicitly with `ORDER BY`.

## 2. Sort from Lowest to Highest with `ASC`

```sql
SELECT title, price_paise
FROM books
ORDER BY price_paise ASC, id ASC;
```

Output:

```text
title|price_paise
SQL Basics|30000
Go Basics|50000
Networks|50000
Linux|70000
```

`ASC` means **ascending**:

- numbers: smallest to largest;
- text: alphabetical order according to the database collation;
- dates and times: oldest to newest.

`ASC` is PostgreSQL's default, but writing it explicitly makes the intention
clear while learning.

Why does the example also use `id ASC`? `Go Basics` and `Networks` have the
same price. PostgreSQL first sorts by `price_paise`; for rows tied on price, it
uses `id` as the tie-breaker.

## 3. Sort from Highest to Lowest with `DESC`

```sql
SELECT title, price_paise
FROM books
ORDER BY price_paise DESC, id ASC;
```

Output:

```text
title|price_paise
Linux|70000
Go Basics|50000
Networks|50000
SQL Basics|30000
```

`DESC` means **descending**:

- numbers: largest to smallest;
- text: reverse alphabetical order;
- dates and times: newest to oldest.

Notice that `DESC` applies only to `price_paise`. The tied rows still use
`id ASC`.

## 4. Sort by More Than One Column

Suppose available books must appear first. Within each availability group,
prices should go from lowest to highest:

```sql
SELECT title, available, price_paise
FROM books
ORDER BY available DESC, price_paise ASC, id ASC;
```

Output:

```text
title|available|price_paise
SQL Basics|t|30000
Go Basics|t|50000
Linux|t|70000
Networks|f|50000
```

Read the ordering from left to right:

1. `available DESC` creates the `TRUE` group followed by the `FALSE` group.
2. `price_paise ASC` sorts rows inside each group.
3. `id ASC` gives equal-price rows a stable tie-breaker.

PostgreSQL displays Boolean `TRUE` as `t` and `FALSE` as `f` in this output
format.

## 5. Return Only Some Rows with `LIMIT`

`LIMIT` sets the maximum number of rows returned:

```sql
SELECT id, title
FROM books
ORDER BY id ASC
LIMIT 2;
```

Output:

```text
id|title
1|Go Basics
2|SQL Basics
```

The complete ordered result has four rows, but `LIMIT 2` returns only its first
two rows.

Always combine pagination with `ORDER BY`. Without an order, “the first two
rows” has no stable meaning.

## 6. Skip Rows with `OFFSET`

`OFFSET` tells PostgreSQL how many rows of the ordered result to skip:

```sql
SELECT id, title
FROM books
ORDER BY id ASC
LIMIT 2
OFFSET 2;
```

Output:

```text
id|title
3|Networks
4|Linux
```

PostgreSQL conceptually performs these steps:

1. order all matching rows by `id`;
2. skip the first two rows;
3. return at most two rows.

For page-number pagination:

```text
offset = (page number - 1) × page size
```

With a page size of `2`:

| Page | `LIMIT` | `OFFSET` | Rows selected |
|---:|---:|---:|---|
| 1 | 2 | 0 | 1–2 |
| 2 | 2 | 2 | 3–4 |
| 3 | 2 | 4 | 5–6 |

`OFFSET 0` can be omitted, so page 1 normally uses only `LIMIT 2`.

## Your Exercise

Do not change the schema, inserted rows, or constraints in `main.sql`. Remove
the old checkpoint 04 queries and write exactly five new queries.

Starting rows:

| `id` | `name` | `price_paise` | `available` |
|---:|---|---:|---|
| 1 | Raagi Malt | 5000 | `TRUE` |
| 2 | Fruit Juice | 8000 | `TRUE` |
| 3 | Sprout Salad | 6500 | `FALSE` |

Write:

1. `name` and `price_paise`, ordered from lowest price to highest. Explicitly
   use `ASC`.
2. `name` and `price_paise`, ordered from highest price to lowest. Use `DESC`.
3. `name`, `available`, and `price_paise`, with available products first and
   prices low to high inside each group.
4. Page 1: `id` and `name`, ordered by `id`, with a page size of two.
5. Page 2: the same columns, order, and page size, skipping page 1.

## Expected Exercise Output

```text
name|price_paise
Raagi Malt|5000
Sprout Salad|6500
Fruit Juice|8000
name|price_paise
Fruit Juice|8000
Sprout Salad|6500
Raagi Malt|5000
name|available|price_paise
Raagi Malt|t|5000
Fruit Juice|t|8000
Sprout Salad|f|6500
id|name
1|Raagi Malt
2|Fruit Juice
id|name
3|Sprout Salad
```

Page 2 contains only one row because the table has three rows and the page size
is two.

## Run and Verify

From `databases`:

```bash
docker compose up -d
docker compose exec postgres \
  psql --username course_user --dbname sql_course
```

Inside `psql`:

```text
\set QUIET on
\pset format unaligned
\pset fieldsep '|'
\pset tuples_only off
\pset footer off
\i main.sql
```

## Acceptance Criteria

- Exactly five exercise queries appear in the required order.
- Every query selects only the requested columns.
- Queries 1 and 2 explicitly use `ASC` and `DESC`.
- Query 3 orders by both `available` and `price_paise`.
- Queries 4 and 5 use the same order and page size.
- Query 5 uses `OFFSET`.
- Two consecutive runs produce the expected output.

## Stop Here

Say `done` when the output matches. Do not start `NULL`, updates, or deletes.
