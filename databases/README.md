# Databases From Scratch

Status: **In progress**

This track teaches the raw SQL needed before returning to the Go HTTP server
track for SQLite, migrations, and SQLC.

## How This Track Works

This is an interactive course, not a long document to read all at once.

For every checkpoint:

1. Read one small lesson.
2. Write its SQL exercise in `main.sql`.
3. Execute the file with SQLite.
4. Ask questions at any point.
5. Say `done` when the exercise works.
6. Codex reviews the SQL and output before creating the next lesson.

Only the current lesson has a full lesson file. Future lessons remain titles in
this roadmap until the current exercise is complete.

Start and completion times are recorded in [`PROGRESS.md`](PROGRESS.md). These
measure wall-clock time, including breaks, so predictions become more reliable
after several checkpoints.

## Exercise Contract

Every lesson must clearly contain:

1. the starting state;
2. the exact input data to use;
3. the exact SQL operations you are expected to write;
4. the deterministic output or final database state;
5. the acceptance criteria and verification commands;
6. a stop point before the next topic.

When you say `done`, Codex will check only that written contract. If the
exercise passes, Codex records the completion time and creates the next small
lesson. If it does not pass, Codex identifies the unchecked requirement.

Learner-chosen input is used only when the values cannot affect verification.
Otherwise, the lesson supplies fixed rows so both the learner and Codex expect
the same result. The roadmap below previews scope; the current lesson file
contains the complete test contract.

## Working Method

```text
edit main.sql
      ↓
execute it with .read main.sql
      ↓
inspect the database with SQLite CLI commands
      ↓
ask questions or submit the result
```

The two important files have different jobs:

```text
main.sql                 SQL source preserved in Git
practice/sql-course.db   disposable database state ignored by Git
```

SQL statements belong in `main.sql`. The SQLite prompt is mainly for commands
such as `.read`, `.tables`, `.schema`, and `.quit`.

## Raw SQL Roadmap

Each lesson should take roughly 30–90 focused minutes. Difficult topics may
need more than one session.

| # | Checkpoint | Exercise you will complete |
|---|---|---|
| 01 | SQL file, CLI, and first table | Create a repeatable `products(id, name)` table and inspect its schema |
| 02 | Insert and read rows | Use one single-row insert and one multi-row insert, then query all columns and only `name` |
| 03 | Protect valid data | Add price and availability constraints, then prove invalid inserts are rejected |
| 04 | Filter rows | Write product queries using comparisons, `AND`, `OR`, and `NOT` |
| 05 | Sort and limit results | Produce ordered results and two predictable pages |
| 06 | Missing values | Store an optional value and query or replace `NULL` safely |
| 07 | Change and remove rows safely | Update and delete targeted rows without modifying unrelated rows |
| 08 | Summarize data | Calculate product counts and price statistics with aggregate functions |
| 09 | Summarize groups | Group products and filter aggregate results with `HAVING` |
| 10 | Model relationships | Create related category and product tables enforced by a foreign key |
| 11 | Combine matching rows | Return products with their category data using `INNER JOIN` |
| 12 | Preserve unmatched rows | Return every category, including empty categories, using `LEFT JOIN` |
| 13 | Design relational schemas | Replace duplicated facts with a normalized multi-table design |
| 14 | Make changes atomic | Commit one transaction and roll back another, then verify both outcomes |
| 15 | Make reads faster | Add a useful index and explain its read/write trade-off |
| 16 | Understand query execution | Compare query plans before and after adding an index |
| 17 | Prepare queries for applications | Write parameterized CRUD query shapes suitable for SQLC |
| 18 | Raw SQL checkpoint | Build and verify a small multi-table schema without a worked solution |

This roadmap covers the practical SQL foundation needed for the first
production-style Go API. Advanced SQL can be learned later when a real project
requires it.

## After the Raw SQL Checkpoint

Return to `go-http-server` and continue in this order:

```text
open SQLite from Go
        ↓
manage schema changes with migrations
        ↓
configure SQLC
        ↓
generate Go code from reviewed SQL
        ↓
build user and authentication APIs
```

SQLC does not replace SQL knowledge. You still write the SQL; SQLC analyzes it
and generates type-safe Go methods.

## Current Lesson

Start with
[`lessons/04-filter-rows.md`](lessons/04-filter-rows.md).

Completed:

- Checkpoint 01: SQL file, CLI, and first table
- Checkpoint 02: Insert and read rows
- Checkpoint 03: Protect valid data

Stop after the current exercise. Do not begin checkpoint 05 until checkpoint 04
has been reviewed.
