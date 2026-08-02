# PostgreSQL From Scratch

Status: **In progress**

This interactive track teaches raw PostgreSQL before the Go HTTP server track
continues with migrations and SQLC.

## Architecture

Only Docker is installed on the host. PostgreSQL and its `psql` client both run
inside the container:

```text
compose.yaml
    └── postgres container
          ├── PostgreSQL server
          ├── psql client
          ├── /workspace/main.sql (read-only bind mount)
          └── /var/lib/postgresql (persistent Docker volume)
```

`main.sql` is source code tracked by Git. Database state lives in the
`postgres-data` Docker volume.

## Start PostgreSQL

From `databases`:

```bash
docker compose up -d
docker compose ps
```

Wait until the service reports `healthy`, then enter `psql`:

```bash
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

Backslash commands belong to `psql` and do not end with semicolons. SQL
statements do end with semicolons.

## Deterministic Output

Lessons use:

```text
\set QUIET on
\pset format unaligned
\pset fieldsep '|'
\pset tuples_only off
\pset footer off
```

This hides command-status noise, prints one row per line, separates columns
with `|`, includes headers, and omits row-count footers.

## Stop or Reset

Stop the container while keeping data:

```bash
docker compose down
```

Delete the container and the entire disposable course database:

```bash
docker compose down --volumes
```

The second command permanently deletes the Docker volume.

## Optional Configuration

The Compose file has working local defaults. To override them:

```bash
cp .env.example .env
```

`.env` is ignored by Git. The example password is only for local development,
not production secret management.

## Learning Workflow

For every checkpoint:

1. Read one small lesson.
2. Write the exercise in `main.sql`.
3. Run it with `\i main.sql`.
4. Compare its output with the fixed contract.
5. Ask questions at any point.
6. Say `done` for review.

Every active lesson specifies fixed inputs, expected output, acceptance
criteria, verification commands, and a stop point.

## Roadmap

| # | Checkpoint | Exercise |
|---|---|---|
| 01 | SQL file, `psql`, and first table | Create and inspect `products(id, name)` |
| 02 | Insert and read rows | Insert rows and select columns |
| 03 | Protect valid data | Add constraints and reject invalid data |
| 04 | Filter rows | Use comparisons, `AND`, `OR`, and `NOT` |
| 05 | Sort and limit results | Use `ORDER BY`, `ASC`, `DESC`, `LIMIT`, and `OFFSET` |
| 06 | Missing values | Store and query `NULL` |
| 07 | Change and remove rows safely | Use targeted `UPDATE` and `DELETE` |
| 08 | Summarize data | Use aggregate functions |
| 09 | Summarize groups | Use `GROUP BY` and `HAVING` |
| 10 | Model relationships | Add a foreign key |
| 11 | Combine matching rows | Use `INNER JOIN` |
| 12 | Preserve unmatched rows | Use `LEFT JOIN` |
| 13 | Design relational schemas | Normalize a schema |
| 14 | Make changes atomic | Use transactions |
| 15 | Make reads faster | Add an index |
| 16 | Understand execution | Compare `EXPLAIN` plans |
| 17 | Prepare for applications | Write parameterized SQLC query shapes |
| 18 | Raw SQL checkpoint | Build a small multi-table schema |

## Current Lesson

Open
[`lessons/13-normalize-a-schema.md`](lessons/13-normalize-a-schema.md).

Completed: checkpoints 01–13. Stop before checkpoint 14 until its lesson is
prepared.

Checkpoint 13 teaches how normalization gives each fact one authoritative
home and prevents update, insert, and delete anomalies.

The exercise designs customers, products, orders, and order items, then
reconstructs this report:

```text
order_id|customer_name|product_name|price_paise|quantity
1|Asha|Raagi Malt|5000|2
1|Asha|Sprout Salad|6500|1
2|Ravi|Fruit Juice|8000|3
```

## After Raw PostgreSQL

```text
connect Go to PostgreSQL
        ↓
run versioned migrations
        ↓
configure SQLC for PostgreSQL
        ↓
generate type-safe Go methods
        ↓
build user and authentication APIs
```

## Official References

- [Docker Compose](https://docs.docker.com/compose/intro/compose-application-model/)
- [Official PostgreSQL image](https://hub.docker.com/_/postgres)
- [`psql`](https://www.postgresql.org/docs/current/app-psql.html)
- [Identity columns](https://www.postgresql.org/docs/current/ddl-identity-columns.html)
- [Boolean type](https://www.postgresql.org/docs/current/datatype-boolean.html)
- [`NULL` comparison functions](https://www.postgresql.org/docs/current/functions-comparison.html)
- [`UPDATE`](https://www.postgresql.org/docs/current/sql-update.html)
- [`DELETE`](https://www.postgresql.org/docs/current/sql-delete.html)
- [`RETURNING`](https://www.postgresql.org/docs/current/dml-returning.html)
- [Aggregate functions](https://www.postgresql.org/docs/current/functions-aggregate.html)
- [Foreign keys](https://www.postgresql.org/docs/current/ddl-constraints.html#DDL-CONSTRAINTS-FK)
- [Joined tables](https://www.postgresql.org/docs/current/queries-table-expressions.html#QUERIES-JOIN)
