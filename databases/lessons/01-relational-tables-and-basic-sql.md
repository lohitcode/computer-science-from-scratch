# Checkpoint 01: SQL File, `psql`, and First Table

Status: **Complete**

## Goal

Write SQL in `main.sql`, execute it through PostgreSQL's `psql` client, and
inspect one table.

## Mental Model

```text
main.sql       SQL source tracked by Git
PostgreSQL     server executing SQL
psql           client sending SQL to the server
Docker volume  persistent table and row data
```

## PostgreSQL Table Shape

Example:

```sql
DROP TABLE IF EXISTS books;

CREATE TABLE books (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    title TEXT NOT NULL
);
```

`GENERATED ALWAYS AS IDENTITY` makes PostgreSQL generate an ID when an insert
omits that column.

## Completed Contract

`products` was created with:

| Column | Definition |
|---|---|
| `id` | Generated integer primary key |
| `name` | Required text |

The disposable exercise drops and recreates `products` so it is repeatable.
Production changes will later use migrations.

## Commands

```bash
docker compose up -d
docker compose exec postgres \
  psql --username course_user --dbname sql_course
```

Inside `psql`:

```text
\i main.sql
\dt
\d products
\q
```

`\i`, `\dt`, `\d`, and `\q` are `psql` meta-commands. SQL statements use
semicolons; these commands do not.
