# Checkpoint 12: Preserve Unmatched Rows with `LEFT JOIN`

Status: **Complete**

## Goal

Learn how to:

- preserve every row from one table with `LEFT JOIN`;
- recognize the `NULL` placeholders created for missing matches;
- count matched child rows correctly;
- avoid accidentally turning a left join into an inner join.

## Mental Model: Keep the Entire Left Side

`INNER JOIN` returns only matching row pairs. `LEFT JOIN` makes an additional
promise:

> Return every row from the table on the left, even when the table on the
> right has no match.

Imagine:

```text
authors                         books
id | name                       id | title            | author_id
1  | Ursula Le Guin             1  | Earthsea         | 1
2  | Octavia Butler             2  | The Dispossessed | 1
3  | J. R. R. Tolkien           3  | Kindred          | 2
```

This query starts from `authors`, so all authors are preserved:

```sql
SELECT
    a.name AS author_name,
    b.title AS book_title
FROM authors AS a
LEFT JOIN books AS b
    ON b.author_id = a.id
ORDER BY a.id, b.id;
```

Output:

```text
author_name|book_title
Ursula Le Guin|Earthsea
Ursula Le Guin|The Dispossessed
Octavia Butler|Kindred
J. R. R. Tolkien|[NULL]
```

Tolkien has no matching book. PostgreSQL still produces one result row and
fills columns from `books` with `NULL`.

## Join Direction Matters

In:

```sql
FROM authors AS a
LEFT JOIN books AS b
```

- `authors` is the preserved table;
- `books` is the optional matching table.

Reversing the tables changes which rows are guaranteed to survive:

```text
all authors, optional books → authors LEFT JOIN books
all books, optional authors → books LEFT JOIN authors
```

Choose the left table from the question you are asking.

## The `COUNT(*)` Trap

A left join creates one output row for an unmatched parent:

```text
J. R. R. Tolkien | [NULL]
```

Therefore, `COUNT(*)` counts that preserved row and incorrectly reports one
book for Tolkien.

Count a non-`NULL` child key instead:

```sql
SELECT
    a.name AS author_name,
    COUNT(b.id) AS book_count
FROM authors AS a
LEFT JOIN books AS b
    ON b.author_id = a.id
GROUP BY a.id, a.name
ORDER BY a.id;
```

Output:

```text
author_name|book_count
Ursula Le Guin|2
Octavia Butler|1
J. R. R. Tolkien|0
```

Why this works:

```text
COUNT(*)    → counts the preserved result row
COUNT(b.id) → ignores NULL when no child matched
```

The child primary key is a good counting target because a real child row can
never have a `NULL` primary key.

## Aggregates Can Return `NULL`

`SUM` over no matching child values returns `NULL`, not zero:

```sql
SUM(b.price_paise)
```

When the desired business meaning is zero, use `COALESCE`:

```sql
COALESCE(SUM(b.price_paise), 0)
```

`COALESCE` returns its first non-`NULL` argument. It preserves real totals and
replaces only the missing total with `0`.

## A `WHERE` Condition Can Remove Preserved Rows

This query loses authors without a matching title:

```sql
SELECT
    a.name,
    b.title
FROM authors AS a
LEFT JOIN books AS b
    ON b.author_id = a.id
WHERE b.title = 'Earthsea';
```

For an unmatched author, `b.title` is `NULL`. The `WHERE` condition is not
true, so that preserved row is removed. The query behaves like an inner join
for this condition.

When the intention is “preserve every author, but match only Earthsea,” put
the child condition in `ON`:

```sql
SELECT
    a.name AS author_name,
    b.title AS book_title
FROM authors AS a
LEFT JOIN books AS b
    ON b.author_id = a.id
   AND b.title = 'Earthsea'
ORDER BY a.id;
```

Output:

```text
author_name|book_title
Ursula Le Guin|Earthsea
Octavia Butler|[NULL]
J. R. R. Tolkien|[NULL]
```

Use this mental model:

```text
ON condition for the right table → controls which rows match
WHERE condition                 → filters the completed join result
```

## Your Exercise

Keep the Lesson 11 schema and seed data unchanged:

- categories: `Drinks`, `Foods`, `Desserts`;
- three products;
- no product in `Desserts`.

Replace the two Lesson 11 inner-join queries with exactly two left-join
queries:

1. Start from `categories AS c` and left join `products AS p`.
   - Match `p.category_id` to `c.id`.
   - Return `c.name AS category_name` and `p.name AS product_name`.
   - Order by `c.id`, then `p.id`.
2. Start from `categories AS c` and left join `products AS p`.
   - Match `p.category_id` to `c.id`.
   - Return:
     - `c.name AS category_name`;
     - `COUNT(p.id) AS product_count`;
     - `COALESCE(SUM(p.price_paise), 0) AS total_price`.
   - Group by `c.id` and `c.name`.
   - Order by `c.id`.

Do not use `COUNT(*)` in the second query. Leave `invalid.sql` unchanged.

## Expected Output

```text
category_name|product_name
Drinks|Raagi Malt
Drinks|Fruit Juice
Foods|Sprout Salad
Desserts|[NULL]
category_name|product_count|total_price
Drinks|2|13000
Foods|1|6500
Desserts|0|0
```

The `Desserts` detail row contains `[NULL]` because no product matched. Its
summary correctly contains a count and total of zero.

## Run and Verify

From `databases`, enter `psql`:

```bash
docker compose exec postgres \
  psql --username course_user --dbname sql_course
```

Configure deterministic output if needed:

```text
\set QUIET on
\pset format unaligned
\pset fieldsep '|'
\pset tuples_only off
\pset footer off
\pset null '[NULL]'
```

Run twice:

```text
\i main.sql
\i main.sql
```

## Acceptance Criteria

- The Lesson 11 schema and seed rows remain unchanged.
- Exactly two result queries use `LEFT JOIN`.
- `categories` is on the left in both queries.
- Both joins match the child foreign key to the parent primary key.
- The first query exposes `[NULL]` for the unmatched product.
- The second query uses `COUNT(p.id)`, not `COUNT(*)`.
- The second query uses `COALESCE` so the missing total becomes zero.
- The output exactly matches on two consecutive runs.

## Stop Here

Say `done` when both runs match. Do not start normalization.
