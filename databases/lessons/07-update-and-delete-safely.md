# Checkpoint 07: Update and Delete Rows Safely

Status: **Complete**

## Goal

Learn to:

- change existing rows with `UPDATE`;
- change multiple columns in one statement;
- remove rows with `DELETE`;
- target rows safely with `WHERE`;
- inspect changed or deleted rows with PostgreSQL's `RETURNING`.

## Example Data

Imagine a `tasks` table containing:

| `id` | `title` | `done` |
|---:|---|---|
| 1 | Learn SQL | `FALSE` |
| 2 | Build API | `FALSE` |
| 3 | Old task | `TRUE` |

## 1. Preview Before Changing Data

First, write a `SELECT` using the same `WHERE` condition that the write
statement will use:

```sql
SELECT id, title, done
FROM tasks
WHERE id = 2;
```

Output:

```text
id|title|done
2|Build API|f
```

This answers an important question before any data changes:

> Which rows will this condition target?

Production code commonly targets a row by its primary key because an ID is
unique and stable. A name or title might not be unique and may itself change.

## 2. Update One Row

The shape of an update is:

```text
UPDATE table
SET column = new_value
WHERE row_condition
RETURNING columns_to_display;
```

Complete example:

```sql
UPDATE tasks
SET done = TRUE
WHERE id = 2
RETURNING id, title, done;
```

Output:

```text
id|title|done
2|Build API|t
```

Read it in this order:

1. `UPDATE tasks` chooses the table.
2. `WHERE id = 2` chooses the row.
3. `SET done = TRUE` changes that row.
4. `RETURNING` displays the row after the change.

`RETURNING` is especially useful in PostgreSQL applications because one query
can change a row and return its new state.

## 3. Update Multiple Columns

Separate assignments with commas:

```sql
UPDATE tasks
SET title = 'Build production API',
    done = TRUE
WHERE id = 2
RETURNING id, title, done;
```

Output:

```text
id|title|done
2|Build production API|t
```

The comma separates assignments. Do not write `SET` twice.

## 4. Delete One Row

Preview the target:

```sql
SELECT id, title
FROM tasks
WHERE id = 3;
```

Output:

```text
id|title
3|Old task
```

Then delete that same target:

```sql
DELETE FROM tasks
WHERE id = 3
RETURNING id, title;
```

Output:

```text
id|title
3|Old task
```

For `DELETE`, `RETURNING` displays the row that existed immediately before it
was removed.

## 5. Why a Missing `WHERE` Is Dangerous

These are valid SQL statements:

```sql
UPDATE tasks
SET done = TRUE;
```

```sql
DELETE FROM tasks;
```

The first changes **every row**. The second removes **every row** while leaving
the table itself in place.

That may occasionally be intentional, but it is dangerous when you meant to
target one row. Build this habit:

```text
write WHERE → preview with SELECT → check the rows → perform the write
```

Transactions will later add another safety layer, but a precise `WHERE`
condition is still essential.

## Your Exercise

Keep the Lesson 06 schema, constraints, and three starting products. Remove
the four Lesson 06 queries and write the following seven statements in order.

### Fixed Operations

1. Preview Raagi Malt by selecting `id`, `name`, and `price_paise` where
   `id = 1`.
2. Update product `id = 1` to set `price_paise` to `5500`. Return `name` and
   `price_paise`.
3. Preview Sprout Salad by selecting `id`, `name`, and `price_paise` where
   `id = 3`.
4. Update product `id = 3` in one statement:
   - set `available` to `TRUE`;
   - set `description` to `Fresh mixed sprouts`;
   - return `name`, `available`, and `description`.
5. Preview the product to be deleted by selecting `id` and `name` where
   `id = 2`.
6. Delete product `id = 2` and return `id` and `name`.
7. Verify the final table by selecting `id`, `name`, `price_paise`,
   `available`, and `description`, ordered by `id ASC`.

Use the exact IDs above. Do not change the starting `INSERT` statements just
to produce the final state.

## Expected Exercise Output

```text
id|name|price_paise
1|Raagi Malt|5000
name|price_paise
Raagi Malt|5500
id|name|price_paise
3|Sprout Salad|6500
name|available|description
Sprout Salad|t|Fresh mixed sprouts
id|name
2|Fruit Juice
id|name
2|Fruit Juice
id|name|price_paise|available|description
1|Raagi Malt|5500|t|Traditional millet drink
3|Sprout Salad|6500|t|Fresh mixed sprouts
```

The final IDs are `1` and `3`. PostgreSQL does not renumber identity values
after row `2` is deleted; IDs identify rows and are not list positions.

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

- The Lesson 06 schema and starting rows remain intact.
- Exactly seven exercise statements appear in the required order.
- Every write target is previewed before its destructive operation.
- Every `UPDATE` and `DELETE` has a `WHERE` clause.
- Both updates and the deletion use `RETURNING`.
- The multi-column update uses one `SET` clause.
- Two consecutive runs produce the expected output.

## Stop Here

Say `done` when the output matches. Do not start aggregate functions.
