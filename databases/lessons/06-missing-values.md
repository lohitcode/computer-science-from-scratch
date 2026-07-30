# Checkpoint 06: Missing Values with `NULL`

Status: **Complete**

## Goal

Learn what `NULL` represents, how it differs from `0` and an empty string, and
how to query nullable columns with:

- `IS NULL`;
- `IS NOT NULL`;
- `COALESCE`.

## 1. What Is `NULL`?

`NULL` means **the value is missing or unknown**.

It is not the number `0`, the Boolean `FALSE`, or the empty string `''`.

Consider this `employees` data:

| `id` | `name` | `phone` | Meaning |
|---:|---|---|---|
| 1 | Asha | `NULL` | Phone number is unknown |
| 2 | Ravi | `''` | A known empty string was stored |
| 3 | Mina | `9876543210` | Phone number is known |

Display `NULL` clearly in `psql`:

```text
\pset null '[NULL]'
```

Now this complete query:

```sql
SELECT name, phone
FROM employees
ORDER BY id ASC;
```

prints:

```text
name|phone
Asha|[NULL]
Ravi|
Mina|9876543210
```

The blank after `Ravi|` is an empty string. `[NULL]` is only how `psql`
displays the missing value; the database does not store the text `[NULL]`.

## 2. Why `= NULL` Does Not Work

This is incorrect:

```sql
SELECT name
FROM employees
WHERE phone = NULL;
```

`NULL` is unknown, so PostgreSQL cannot say that one unknown value equals
another. The comparison produces the logical result `UNKNOWN`, not `TRUE`.
A `WHERE` clause keeps only rows whose condition is `TRUE`.

Use the special predicate `IS NULL`:

```sql
SELECT name
FROM employees
WHERE phone IS NULL
ORDER BY id ASC;
```

Output:

```text
name
Asha
```

Mental model:

```text
ordinary known value → compare with =, <, >, and so on
missing value        → test with IS NULL or IS NOT NULL
```

## 3. Find Values That Are Present

```sql
SELECT name
FROM employees
WHERE phone IS NOT NULL
ORDER BY id ASC;
```

Output:

```text
name
Ravi
Mina
```

Ravi is included because an empty string is still a known, non-`NULL` value.

## 4. Replace `NULL` Only in Query Output

`COALESCE` returns the first non-`NULL` argument:

```sql
SELECT name, COALESCE(phone, 'Phone unavailable') AS phone
FROM employees
ORDER BY id ASC;
```

Output:

```text
name|phone
Asha|Phone unavailable
Ravi|
Mina|9876543210
```

`COALESCE` changes this query's result, not the stored row. It replaces Asha's
`NULL`, but it does not replace Ravi's empty string.

## Your Exercise

Continue using the `products` table in `main.sql`.

### Fixed Input

1. Add this nullable column to `CREATE TABLE`:

   ```sql
   description TEXT
   ```

   Do not add `NOT NULL` or a default.

2. Store these exact description inputs:

   | Product | Description input |
   |---|---|
   | Raagi Malt | `Traditional millet drink` |
   | Fruit Juice | omit the column so PostgreSQL stores `NULL` |
   | Sprout Salad | an empty string: `''` |

3. Remove the five checkpoint 05 queries. Keep the schema, constraints, and
   three products.

### Write Four Queries

1. Select `name` and `description` for every product, ordered by `id`.
2. Select `name` only where `description IS NULL`, ordered by `id`.
3. Select `name` only where `description IS NOT NULL`, ordered by `id`.
4. Select `name` and a displayed description for every product, ordered by
   `id`. Use `COALESCE` to display `Description unavailable` for `NULL`, and
   name the result column `description`.

## Expected Exercise Output

First run `\pset null '[NULL]'`, then run `main.sql`. The exact output is:

```text
name|description
Raagi Malt|Traditional millet drink
Fruit Juice|[NULL]
Sprout Salad|
name
Fruit Juice
name
Raagi Malt
Sprout Salad
name|description
Raagi Malt|Traditional millet drink
Fruit Juice|Description unavailable
Sprout Salad|
```

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

- `description` is nullable.
- The three rows contain the exact fixed inputs.
- Exactly four exercise queries appear in the required order.
- No query uses `= NULL` or `!= NULL`.
- Queries 2 and 3 use `IS NULL` and `IS NOT NULL`.
- Query 4 uses `COALESCE` and aliases its result as `description`.
- Two consecutive runs produce the expected output.

## Stop Here

Say `done` when the output matches. Do not start `UPDATE` or `DELETE`.
