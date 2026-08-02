# Checkpoint 11: Combine Matching Rows with `INNER JOIN`

Status: **Complete**

## Goal

Learn how to:

- combine related rows from two tables;
- describe the match with `ON`;
- qualify columns with table aliases;
- recognize that `INNER JOIN` removes unmatched rows.

## Why a Join Is Needed

Lesson 10 deliberately separated categories from products:

```text
products.category_id → categories.id
```

That design avoids repeating category names, but a product query now contains
only an ID. To display the category name, PostgreSQL must combine the related
rows.

A foreign key protects the relationship when data is written. A join follows
the relationship when data is read.

## Mental Model: Match Row Pairs

Imagine these tables:

```text
authors                         books
id | name                       id | title            | author_id
1  | Ursula Le Guin             1  | Earthsea         | 1
2  | Octavia Butler             2  | The Dispossessed | 1
3  | J. R. R. Tolkien           3  | Kindred          | 2
```

For each candidate pair, the join checks:

```text
authors.id = books.author_id
```

Matching pairs become result rows:

```text
author 1 + book 1
author 1 + book 2
author 2 + book 3
```

Author 3 has no matching book, so an inner join does not produce a row for
that author.

## 1. Write an `INNER JOIN`

```sql
SELECT
    b.title AS book_title,
    a.name AS author_name
FROM books AS b
INNER JOIN authors AS a
    ON a.id = b.author_id
ORDER BY b.id;
```

Output:

```text
book_title|author_name
Earthsea|Ursula Le Guin
The Dispossessed|Ursula Le Guin
Kindred|Octavia Butler
```

Read the query in this order:

```text
FROM books AS b
    start with book rows

INNER JOIN authors AS a
    find matching author rows

ON a.id = b.author_id
    define what "matching" means
```

The equality usually connects:

```text
parent primary key = child foreign key
```

### `JOIN` Means `INNER JOIN`

In PostgreSQL, a bare `JOIN` is shorthand for `INNER JOIN`. These two queries
have exactly the same meaning:

```sql
FROM books AS b
INNER JOIN authors AS a ON a.id = b.author_id
```

```sql
FROM books AS b
JOIN authors AS a ON a.id = b.author_id
```

`INNER JOIN` is useful when teaching or when you want the join type to be
visually explicit. `JOIN` is common in application queries because it is
shorter. Neither version is faster; PostgreSQL parses them as the same kind of
join.

The shorthand applies specifically to an inner join. Continue to write other
join types explicitly, such as `LEFT JOIN`.

## 2. Use Table Aliases to Remove Ambiguity

Both tables contain columns such as `id` and `name`-like values. A bare `id`
would be ambiguous after the tables are combined.

Aliases give each table a short local name:

```sql
books AS b
authors AS a
```

Then qualify columns:

```sql
b.id
b.title
a.id
a.name
```

`AS` is optional for table aliases in PostgreSQL, but writing it while
learning makes the alias declaration explicit.

## 3. `ON` Connects Tables; `WHERE` Filters Results

```sql
SELECT
    b.title AS book_title,
    a.name AS author_name
FROM books AS b
INNER JOIN authors AS a
    ON a.id = b.author_id
WHERE a.name = 'Ursula Le Guin'
ORDER BY b.id;
```

Output:

```text
book_title|author_name
Earthsea|Ursula Le Guin
The Dispossessed|Ursula Le Guin
```

Keep this mental distinction:

```text
ON     → How are the two tables related?
WHERE  → Which joined result rows do I want?
```

## 4. Aggregate the Matched Rows

Joins can feed the operations you already learned:

```sql
SELECT
    a.name AS author_name,
    COUNT(*) AS book_count
FROM authors AS a
INNER JOIN books AS b
    ON b.author_id = a.id
GROUP BY a.id, a.name
ORDER BY a.id;
```

Output:

```text
author_name|book_count
Ursula Le Guin|2
Octavia Butler|1
```

Tolkien is absent because no joined row exists for that author. Lesson 12
will preserve unmatched parent rows with `LEFT JOIN`.

## Common Mistakes

### Missing the `ON` Condition

If every row from one table is paired with every row from the other, the
result is a Cartesian product. With 3 authors and 3 books, that would produce
9 pairs rather than 3 correct matches.

### Matching Unrelated Columns

This is syntactically valid but logically wrong:

```sql
ON a.id = b.id
```

The relationship is stored in `b.author_id`, so the correct match is:

```sql
ON a.id = b.author_id
```

Column names do not automatically create the relationship. The `ON`
expression must follow the schema's keys.

### Assuming Output Order

A join does not guarantee result order. Add `ORDER BY` whenever the order is
part of the output contract.

## Your Exercise

Keep the Lesson 10 schemas and constraints.

### Change the Seed Data

Add `Desserts` as the third category, so the categories are inserted in this
exact order:

1. `Drinks`
2. `Foods`
3. `Desserts`

Keep the same three products. No product should reference category `3`.

Replace the two Lesson 10 `SELECT` statements with exactly two join queries:

1. Start from `products` aliased as `p` and inner join `categories` aliased as
   `c`.
   - Match `c.id` to `p.category_id`.
   - Return `p.id AS product_id`, `p.name AS product_name`, and
     `c.name AS category_name`.
   - Order by `p.id`.
2. Start from `categories` aliased as `c` and inner join `products` aliased as
   `p`.
   - Match `p.category_id` to `c.id`.
   - Return `c.name AS category_name`, `COUNT(*) AS product_count`, and
     `SUM(p.price_paise) AS total_price`.
   - Group by both `c.id` and `c.name`.
   - Order by `c.id`.

Do not use `LEFT JOIN` yet. Leave `invalid.sql` unchanged; it should still
test the orphan foreign key from Lesson 10.

## Expected Output

```text
product_id|product_name|category_name
1|Raagi Malt|Drinks
2|Fruit Juice|Drinks
3|Sprout Salad|Foods
category_name|product_count|total_price
Drinks|2|13000
Foods|1|6500
```

`Desserts` does not appear. It exists in `categories`, but `INNER JOIN`
returns only matching row pairs.

## Run and Verify

From `databases`, enter `psql`:

```bash
docker compose exec postgres \
  psql --username course_user --dbname sql_course
```

Configure deterministic output if this is a new session:

```text
\set QUIET on
\pset format unaligned
\pset fieldsep '|'
\pset tuples_only off
\pset footer off
\pset null '[NULL]'
```

Run:

```text
\i main.sql
```

Also confirm the unmatched category really exists:

```sql
SELECT id, name
FROM categories
ORDER BY id;
```

Expected check:

```text
id|name
1|Drinks
2|Foods
3|Desserts
```

Run `main.sql` twice.

## Acceptance Criteria

- The schemas and constraints from Lesson 10 remain intact.
- `Desserts` exists as category `3` and has no product.
- Exactly two result queries use `INNER JOIN`.
- Both joins match the primary key to the foreign key.
- Selected columns are qualified with the required aliases.
- The second query groups and aggregates the matched products correctly.
- Neither query uses `LEFT JOIN`.
- The exact expected output is produced on two consecutive runs.

## Stop Here

Say `done` when both runs match. Do not start `LEFT JOIN`.
