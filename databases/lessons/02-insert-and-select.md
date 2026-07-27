# Checkpoint 02: Insert and Select Rows

Status: **Complete**

## Goal

Insert rows, retrieve all columns, and retrieve one chosen column.

## Completed Contract

Fixed rows:

| Insert style | `name` |
|---|---|
| Individual | Raagi Malt |
| Multi-row, first | Fruit Juice |
| Multi-row, second | Sprout Salad |

The inserts omit `id`, so PostgreSQL's identity column generates `1`, `2`, and
`3` after the table is recreated.

Required queries:

```sql
SELECT * FROM products;
SELECT name FROM products;
```

## Mental Model

```text
CREATE TABLE → define structure
INSERT       → store rows
SELECT       → retrieve rows
```

Example:

```sql
INSERT INTO books (title)
VALUES ('The Go Programming Language');

INSERT INTO books (title)
VALUES
    ('Designing Data-Intensive Applications'),
    ('The C Programming Language');
```

Text values use single quotes. Every parenthesized values group becomes one
row.

## Completed Output

With tuples-only output enabled:

```text
1|Raagi Malt
2|Fruit Juice
3|Sprout Salad
Raagi Malt
Fruit Juice
Sprout Salad
```

The script can be executed repeatedly without duplicating rows because it
recreates the table first.
