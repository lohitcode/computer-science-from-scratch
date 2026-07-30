# Checkpoint 10: Model Relationships with Foreign Keys

Status: **Complete**

## Goal

Learn how to:

- model a one-to-many relationship with two tables;
- identify parent and child tables;
- connect them with a foreign key;
- let PostgreSQL prevent orphan rows.

This lesson stores the relationship. Lesson 11 will read related data with a
join.

## Why Relational Databases Use Keys

Suppose every product stores its category as repeated text:

| Product | Category |
|---|---|
| Raagi Malt | Drinks |
| Fruit Juice | Drinks |
| Sprout Salad | Foods |

The word `Drinks` is duplicated. A typo such as `Drink` creates an accidental
new category, and renaming a category requires changing many rows.

The relational model gives the category its own row and identity:

```text
categories
1 | Drinks
2 | Foods

products
Raagi Malt   | category_id 1
Fruit Juice  | category_id 1
Sprout Salad | category_id 2
```

The product stores the category's key, not another copy of its name.

This idea comes from the relational model: rows are connected through values,
so applications do not need physical pointers between records.

## Mental Model: Parent, Child, and Reference

Consider authors and books:

```text
authors                       books
id | name                     id | title       | author_id
1  | Ursula Le Guin           1  | Earthsea    | 1
                               2  | The Dispossessed | 1
```

- `authors` is the **parent** table.
- `books` is the **child** table.
- `authors.id` is the parent's primary key.
- `books.author_id` is a foreign key that references it.

One author can be referenced by many books, but each book row has one
`author_id`. This is a **one-to-many** relationship.

## 1. A Primary Key Identifies One Parent Row

```sql
CREATE TABLE authors (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);
```

A primary key is both:

- `UNIQUE`: two authors cannot have the same `id`;
- `NOT NULL`: every author must have an identity.

Other tables can safely refer to that stable identity.

## 2. A Foreign Key Restricts Child Values

```sql
CREATE TABLE books (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    title TEXT NOT NULL,
    author_id INTEGER NOT NULL REFERENCES authors(id)
);
```

This part creates the relationship:

```sql
author_id INTEGER NOT NULL REFERENCES authors(id)
```

PostgreSQL now accepts an `author_id` only when the matching `authors.id`
exists. `NOT NULL` additionally says that every book must have an author.

The foreign-key column and referenced column should use compatible types. Here
both are `INTEGER`.

## 3. Insert the Parent Before the Child

```sql
INSERT INTO authors (name)
VALUES ('Ursula Le Guin');

INSERT INTO books (title, author_id)
VALUES ('Earthsea', 1);
```

The author must exist before a book can reference author `1`.

This invalid insert is rejected:

```sql
INSERT INTO books (title, author_id)
VALUES ('Orphan Book', 999);
```

Expected error shape:

```text
ERROR:  insert or update on table "books" violates foreign key constraint
DETAIL:  Key (author_id)=(999) is not present in table "authors".
```

The exact generated constraint name may vary. The important fact is that the
row is rejected because parent `999` does not exist.

## 4. Drop the Child Before the Parent

When rerunning a file, reverse the dependency order:

```sql
DROP TABLE IF EXISTS books;
DROP TABLE IF EXISTS authors;
```

`books` depends on `authors`, so PostgreSQL may refuse to drop `authors` first.

The general pattern is:

```text
create: parent → child
insert: parent → child
drop:   child  → parent
```

## 5. What Happens When a Parent Is Deleted?

Without an `ON DELETE` rule, PostgreSQL prevents deletion of a parent that is
still referenced. This protects existing child rows from becoming orphans.

Later, a schema may deliberately choose a policy such as:

- `ON DELETE RESTRICT`: refuse the parent deletion;
- `ON DELETE CASCADE`: automatically delete its children;
- `ON DELETE SET NULL`: keep children but clear the reference.

Those policies express business rules. Do not choose `CASCADE` merely for
convenience.

## Your Exercise

Replace the current Lesson 09 schema and queries in `main.sql`.

### Part A: `main.sql`

1. Keep `SET client_min_messages TO WARNING;`.
2. Drop `products` first and then `categories`, both with `IF EXISTS`.
3. Create `categories` with:
   - generated integer identity `id` as the primary key;
   - `name TEXT NOT NULL UNIQUE`.
4. Create `products` with:
   - generated integer identity `id` as the primary key;
   - `name TEXT NOT NULL UNIQUE`;
   - `price_paise INTEGER NOT NULL` with a non-negative check;
   - `category_id INTEGER NOT NULL` referencing `categories(id)`.
5. Insert these categories in one statement and in this order:
   - `Drinks`
   - `Foods`
6. Insert these products in one statement and in this order:

| Product | `price_paise` | `category_id` |
|---|---:|---:|
| Raagi Malt | 5000 | 1 |
| Fruit Juice | 8000 | 1 |
| Sprout Salad | 6500 | 2 |

7. Select category `id` and `name`, ordered by `id`.
8. Select product `id`, `name`, and `category_id`, ordered by `id`.

Do not use a join yet.

### Part B: `invalid.sql`

Replace its previous exercise with exactly one insert:

- product name: `Orphan Product`;
- price: `1000`;
- `category_id`: `999`.

Do not add cleanup SQL to `invalid.sql`. PostgreSQL must reject this row.

## Expected `main.sql` Output

```text
id|name
1|Drinks
2|Foods
id|name|category_id
1|Raagi Malt|1
2|Fruit Juice|1
3|Sprout Salad|2
```

## Expected `invalid.sql` Result

The statement must fail with an error containing:

```text
violates foreign key constraint
Key (category_id)=(999) is not present in table "categories".
```

Then this check must return zero:

```sql
SELECT COUNT(*) AS orphan_count
FROM products
WHERE category_id = 999;
```

Expected output:

```text
orphan_count
0
```

## Run and Verify

From `databases`, enter `psql`:

```bash
docker compose exec postgres \
  psql --username course_user --dbname sql_course
```

Configure deterministic output:

```text
\set QUIET on
\pset format unaligned
\pset fieldsep '|'
\pset tuples_only off
\pset footer off
\pset null '[NULL]'
```

Run the valid setup:

```text
\i main.sql
```

Run the deliberately invalid insert:

```text
\i invalid.sql
```

Verify that no orphan was stored:

```sql
SELECT COUNT(*) AS orphan_count
FROM products
WHERE category_id = 999;
```

Run `main.sql` a second time to prove that the setup is repeatable.

## Acceptance Criteria

- There are separate `categories` and `products` tables.
- Both tables have generated identity primary keys.
- `products.category_id` is `NOT NULL` and references `categories(id)`.
- Tables are dropped child-first and created parent-first.
- Parents are inserted before children.
- The valid output exactly matches the expected output.
- No join appears yet.
- The orphan insert fails, and the orphan count remains zero.
- Two consecutive `main.sql` runs produce the same output.

## Stop Here

Say `done` after both the valid and invalid checks behave as expected. Do not
start joins.
