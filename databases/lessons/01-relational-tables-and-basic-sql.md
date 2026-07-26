# Checkpoint 01: SQL File, CLI, and First Table

## Goal

In this checkpoint, do only three things:

1. write SQL in `databases/main.sql`;
2. execute that file with SQLite;
3. create and inspect one table.

Do not insert data yet. That is checkpoint 02.

## Why Use a Table?

A text file could contain:

```text
1,Ragi Malt
2,Fruit Juice
```

But the file does not explain what each position means or which values are
required.

A relational database adds a **schema**: rules describing the shape of the
data.

```text
table    a named collection, such as products
column   one property, such as name
row      one stored product
schema   the structure and rules of the table
```

Today you will create the structure. Rows come next.

## SQL Source Versus Database State

You will have two different files:

```text
main.sql                 instructions written by you
practice/sql-course.db   database state created by SQLite
```

`main.sql` is readable source code and belongs in Git.

`sql-course.db` stores the current tables and rows. It is generated runtime
state and is ignored by Git.

The mental model is:

```text
main.sql tells SQLite what to do
SQLite changes sql-course.db
```

## The `CREATE TABLE` Shape

Here is a complete example for a different table:

```sql
DROP TABLE IF EXISTS books;

CREATE TABLE books (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL
);
```

Read it piece by piece:

```text
DROP TABLE IF EXISTS books
    remove the old practice table so the file can be run again

CREATE TABLE books
    create a table named books

id INTEGER PRIMARY KEY
    create an integer column that uniquely identifies each row

title TEXT NOT NULL
    create a text column that cannot be missing
```

Commas separate column definitions. The semicolon ends an SQL statement.

The `DROP TABLE` line is safe for this disposable practice database. Real
production schema changes will later use migrations.

## Your Exercise

Create `databases/main.sql`.

In that file, define a table named `products` with exactly these columns:

| Column | Required definition |
|---|---|
| `id` | Integer primary key |
| `name` | Required text |

Also make the script repeatable by dropping `products` first if it already
exists.

Do not copy the finished `books` statement unchanged. Translate the schema
requirements into your own `products` statement.

## Execute the File

From the repository root:

```bash
cd databases
mkdir -p practice
sqlite3 practice/sql-course.db
```

You are now inside the SQLite CLI. Run:

```text
.read main.sql
.tables
.schema products
```

Important distinction:

```text
.read main.sql    CLI command: execute an SQL file
.tables           CLI command: list tables
.schema products  CLI command: display the table definition
```

Dot commands belong to the SQLite CLI, so they do not use semicolons.

Exit with:

```text
.quit
```

## Expected Result

- `.read main.sql` finishes without an error.
- `.tables` includes `products`.
- `.schema products` displays your two columns and their rules.
- Running `.read main.sql` a second time also succeeds.

## Check Your Understanding

Before saying `done`, make sure you can answer:

1. What is the difference between `main.sql` and `sql-course.db`?
2. What is a schema?
3. What do table, column, and row mean?
4. Why does `main.sql` begin by dropping the practice table?
5. What is the difference between an SQL statement and a SQLite dot command?

## Stop Here

Send me:

1. your `main.sql`;
2. the output of `.tables`;
3. the output of `.schema products`.

Ask immediately if anything is unclear. Once this checkpoint works, I will
review it and create checkpoint 02 for inserting and selecting rows.
