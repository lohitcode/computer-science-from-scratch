# Checkpoint 05: Sort and Limit Results

Status: **In progress**

## Goal

Use `ORDER BY` to guarantee row order, then use `LIMIT` and `OFFSET` for two
predictable pages.

Do not change the schema, rows, or existing constraints. Do not filter, update,
or delete data.

## Starting State

| `id` | `name` | `price_paise` | `available` |
|---:|---|---:|---|
| 1 | Raagi Malt | 5000 | `TRUE` |
| 2 | Fruit Juice | 8000 | `TRUE` |
| 3 | Sprout Salad | 6500 | `FALSE` |

Keep the schema and inserts in `main.sql`. Replace the checkpoint 04 queries
with the five queries below.

## Required Queries

1. Select `name` and `price_paise`, from lowest price to highest.
2. Select `name` and `price_paise`, from highest price to lowest.
3. Select `name`, `available`, and `price_paise`. Put available products first,
   then order each availability group from lowest price to highest.
4. Select `id` and `name` for page 1: order by `id` and return two rows.
5. Select `id` and `name` for page 2: use the same order and page size, skip
   page 1, and return the next two rows.

Use `ASC` in query 1, `DESC` in query 2, two ordering columns in query 3,
`LIMIT` in queries 4–5, and `OFFSET` in query 5.

## Expected Output

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

Page 2 contains one row because the table has three rows and the page size is
two.

## Mental Model

Without `ORDER BY`, PostgreSQL does not promise result order.

```sql
ORDER BY in_stock DESC, page_count ASC
```

PostgreSQL orders by the first expression. Rows tied on that expression are
ordered by the second expression.

```sql
ORDER BY id ASC
LIMIT 10
OFFSET 20
```

This skips 20 rows and returns at most 10. Pagination needs a deterministic
order.

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

- Exactly five queries appear in the required order.
- Every query selects only the requested columns.
- Queries 1 and 2 explicitly use `ASC` and `DESC`.
- Query 3 orders by `available` and `price_paise`.
- Queries 4 and 5 use the same order and page size.
- Query 5 uses `OFFSET`.
- Output matches the transcript on two runs.

## Stop Here

Say `done` when the output matches. Do not start `NULL`, updates, or deletes.
