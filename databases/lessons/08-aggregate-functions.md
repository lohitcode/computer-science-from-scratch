# Checkpoint 08: Summarize Data with Aggregate Functions

Status: **Complete**

## Goal

Learn how to turn many input rows into summary values with:

- `COUNT`;
- `MIN`;
- `MAX`;
- `SUM`;
- `AVG`.

This lesson summarizes the entire result set. Checkpoint 09 will summarize
separate groups with `GROUP BY`.

## Mental Model: Many Rows Become One Summary

A normal column expression runs once per row:

```sql
SELECT amount_paise
FROM orders;
```

An aggregate function consumes values from multiple rows and produces one
summary:

```sql
SELECT SUM(amount_paise)
FROM orders;
```

Imagine this `orders` table:

| `id` | `amount_paise` |
|---:|---:|
| 1 | 1200 |
| 2 | 800 |
| 3 | `NULL` |
| 4 | 2000 |

## 1. Count Rows with `COUNT(*)`

```sql
SELECT COUNT(*) AS order_count
FROM orders;
```

Output:

```text
order_count
4
```

`COUNT(*)` counts rows. It counts row 3 even though that row's amount is
`NULL`.

## 2. Count Known Values with `COUNT(column)`

```sql
SELECT COUNT(amount_paise) AS orders_with_amount
FROM orders;
```

Output:

```text
orders_with_amount
3
```

`COUNT(amount_paise)` counts only non-`NULL` values in that column.

```text
COUNT(*)       → How many rows exist?
COUNT(column)  → How many rows have a known value in this column?
```

An empty string is a known value, so `COUNT(text_column)` counts it.

## 3. Find the Minimum and Maximum

```sql
SELECT
    MIN(amount_paise) AS smallest_amount,
    MAX(amount_paise) AS largest_amount
FROM orders;
```

Output:

```text
smallest_amount|largest_amount
800|2000
```

`MIN` and `MAX` ignore `NULL`. They work with numbers, text, dates, and other
types that PostgreSQL can order.

## 4. Calculate a Total with `SUM`

```sql
SELECT SUM(amount_paise) AS total_amount
FROM orders;
```

Output:

```text
total_amount
4000
```

`SUM` adds the known amounts: `1200 + 800 + 2000`.

## 5. Calculate an Average with `AVG`

```sql
SELECT ROUND(AVG(amount_paise), 2) AS average_amount
FROM orders;
```

Output:

```text
average_amount
1333.33
```

`AVG` ignores the `NULL` amount. It calculates:

```text
4000 ÷ 3 = 1333.33
```

It does not divide by four. `ROUND(..., 2)` keeps two digits after the decimal
point for predictable display.

## Important `NULL` Rule

These aggregates ignore `NULL` inputs:

```text
COUNT(column), MIN, MAX, SUM, AVG
```

`COUNT(*)` is different because it counts rows, not values.

If no rows match:

- `COUNT` returns `0`;
- `SUM`, `AVG`, `MIN`, and `MAX` return `NULL`.

## Why a Normal Column Cannot Be Mixed In Yet

This query is invalid:

```sql
SELECT id, COUNT(*)
FROM orders;
```

`COUNT(*)` asks for one summary row, while `id` could have many different
values. PostgreSQL does not know which `id` belongs beside the count.

Checkpoint 09 introduces `GROUP BY`, which defines how per-row columns and
aggregates can be combined.

## Your Exercise

Keep the Lesson 06 schema, constraints, and three original `INSERT`
statements. Remove all seven Lesson 07 statements so no product is updated or
deleted.

Starting values:

| Product | `price_paise` | `description` |
|---|---:|---|
| Raagi Malt | 5000 | `Traditional millet drink` |
| Fruit Juice | 8000 | `NULL` |
| Sprout Salad | 6500 | empty string |

Write exactly five queries:

1. Count all rows with `COUNT(*)`. Name the result `product_count`.
2. Count non-`NULL` descriptions with `COUNT(description)`. Name the result
   `products_with_description`.
3. Return the minimum and maximum prices in one query. Name them
   `lowest_price` and `highest_price`.
4. Sum all prices. Name the result `total_price`.
5. Average all prices, rounded to two decimal places. Name the result
   `average_price`.

## Expected Exercise Output

```text
product_count
3
products_with_description
2
lowest_price|highest_price
5000|8000
total_price
19500
average_price
6500.00
```

The description count is `2`: Raagi Malt has text, Fruit Juice has `NULL`, and
Sprout Salad has an empty—but non-`NULL`—string.

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

- The original three products remain unchanged.
- Exactly five aggregate queries appear in the required order.
- Every result column uses the requested alias.
- The description query uses `COUNT(description)`, not `COUNT(*)`.
- Minimum and maximum appear in one query.
- The average is rounded to two decimal places.
- No query uses `GROUP BY`.
- Two consecutive runs produce the expected output.

## Stop Here

Say `done` when the output matches. Do not start `GROUP BY`.
