# Checkpoint 09: Summarize Groups with `GROUP BY` and `HAVING`

Status: **Complete**

## Goal

Learn how to:

- split rows into groups with `GROUP BY`;
- calculate one aggregate result per group;
- filter input rows with `WHERE`;
- filter completed groups with `HAVING`.

## Mental Model: Make Buckets, Then Summarize Each Bucket

Lesson 08 treated the whole table as one group:

```sql
SELECT COUNT(*)
FROM orders;
```

`GROUP BY` first puts rows with the same value into separate buckets. The
aggregate functions then run once for each bucket.

Imagine this `orders` table:

| `id` | `status` | `amount_paise` |
|---:|---|---:|
| 1 | `paid` | 1200 |
| 2 | `paid` | 800 |
| 3 | `pending` | 2000 |
| 4 | `paid` | 1500 |
| 5 | `pending` | 500 |

Conceptually:

```text
paid bucket     → 1200, 800, 1500
pending bucket  → 2000, 500
```

## 1. Create One Result Row per Group

```sql
SELECT
    status,
    COUNT(*) AS order_count,
    SUM(amount_paise) AS total_amount
FROM orders
GROUP BY status
ORDER BY status;
```

Output:

```text
status|order_count|total_amount
paid|3|3500
pending|2|2500
```

`GROUP BY status` creates one group for each distinct status. `COUNT` and
`SUM` then summarize each status separately.

`ORDER BY` is still required when the output order must be predictable.
`GROUP BY` does not promise a display order.

## 2. The Grouping Rule

After grouping, every selected expression must be either:

1. included in `GROUP BY`; or
2. calculated with an aggregate function.

This is valid:

```sql
SELECT status, COUNT(*)
FROM orders
GROUP BY status;
```

This is invalid:

```sql
SELECT status, id, COUNT(*)
FROM orders
GROUP BY status;
```

One status group can contain several different IDs, so PostgreSQL cannot
choose a single `id` for that group's result row.

## 3. Filter Groups with `HAVING`

Suppose you only want statuses containing at least three orders:

```sql
SELECT
    status,
    COUNT(*) AS order_count
FROM orders
GROUP BY status
HAVING COUNT(*) >= 3
ORDER BY status;
```

Output:

```text
status|order_count
paid|3
```

`HAVING` runs after the groups and their aggregate values exist. That is why
it can test `COUNT(*)`.

## 4. `WHERE` and `HAVING` Answer Different Questions

```text
WHERE   → Which individual rows enter the groups?
HAVING  → Which completed groups remain in the result?
```

For example, first keep orders worth at least 1000 paise, then summarize the
remaining rows:

```sql
SELECT
    status,
    COUNT(*) AS order_count,
    SUM(amount_paise) AS total_amount
FROM orders
WHERE amount_paise >= 1000
GROUP BY status
ORDER BY status;
```

Output:

```text
status|order_count|total_amount
paid|2|2700
pending|1|2000
```

Use `WHERE` for ordinary row conditions even when a query also has grouping.
Use `HAVING` when the condition depends on a group or aggregate result.

## Useful Logical Order

Although SQL is written starting with `SELECT`, this mental execution order
explains the behavior:

```text
FROM
  ↓
WHERE
  ↓
GROUP BY
  ↓
HAVING
  ↓
SELECT
  ↓
ORDER BY
```

## Your Exercise

Keep the Lesson 08 table and the same three original products:

| Product | `price_paise` | `available` |
|---|---:|---|
| Raagi Malt | 5000 | `TRUE` |
| Fruit Juice | 8000 | `TRUE` |
| Sprout Salad | 6500 | `FALSE` |

Remove the five Lesson 08 aggregate queries. Do not change the schema or
product rows.

Write exactly three new queries, in this order:

1. Group by `available`. Return `available` and `COUNT(*)` as
   `product_count`. Order by `available DESC`.
2. Group by `available`. Return `available`, `MIN(price_paise)` as
   `lowest_price`, and `MAX(price_paise)` as `highest_price`. Order by
   `available DESC`.
3. Group by `available`. Return `available`, `COUNT(*)` as `product_count`,
   and `SUM(price_paise)` as `total_price`. Keep only groups whose count is
   greater than `1`, then order by `available DESC`.

PostgreSQL's unaligned `psql` output displays booleans as `t` and `f`.

## Expected Exercise Output

```text
available|product_count
t|2
f|1
available|lowest_price|highest_price
t|5000|8000
f|6500|6500
available|product_count|total_price
t|2|13000
```

The last query returns only the `TRUE` group because it has two rows. The
`FALSE` group has one row and fails `HAVING COUNT(*) > 1`.

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
\pset null '[NULL]'
\i main.sql
```

## Acceptance Criteria

- The original schema and three product rows remain unchanged.
- Exactly three result queries appear in the required order.
- Every non-aggregate selected column appears in `GROUP BY`.
- The aliases match the requested names.
- The third query uses `HAVING COUNT(*) > 1`, not `WHERE`.
- Every query uses `ORDER BY available DESC`.
- Two consecutive runs produce the expected output.

## Stop Here

Say `done` when the output matches. Do not start foreign keys.
