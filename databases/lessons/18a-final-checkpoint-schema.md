# Checkpoint 18A: Build a Schema from a Contract

Status: **Complete — Stage A**

Started: **2026-08-06 08:25 IST**

Completed: **2026-08-06 09:18 IST**

Wall time: **53m**

## Goal

This is the final raw-SQL checkpoint. It is split into small stages so you can
implement and verify one concern at a time.

Stage A tests whether you can turn a written business contract into normalized
PostgreSQL tables, seed them deterministically, and reconstruct a report with a
multi-table join. It introduces no new SQL syntax.

Do not copy the previous ordering schema mechanically. First decide which fact
belongs to which entity and which table must exist before another table can
reference it.

## Business Contract

Build a small bookstore database with these relationships:

```text
one author   → many books
one customer → many orders
one order    → many order items
one book     → many order items
```

An order item records the price charged at purchase time. That value may differ
from the book's current price later, so both prices are legitimate facts rather
than accidental duplication.

## Required Tables

Create exactly these five tables.

### `authors`

| Column | Contract |
|---|---|
| `id` | generated identity primary key |
| `name` | required and unique text |

### `books`

| Column | Contract |
|---|---|
| `id` | generated identity primary key |
| `isbn` | required and unique text |
| `title` | required text |
| `author_id` | required reference to `authors(id)` |
| `price_paise` | required integer, zero or greater |

### `customers`

| Column | Contract |
|---|---|
| `id` | generated identity primary key |
| `name` | required text |
| `email` | required and unique text |

### `orders`

| Column | Contract |
|---|---|
| `id` | generated identity primary key |
| `customer_id` | required reference to `customers(id)` |
| `status` | required text limited to `pending`, `paid`, or `cancelled` |

Use a `CHECK` constraint with `IN (...)` for the allowed statuses. The general
shape, using unrelated values, is:

```sql
CHECK (state IN ('open', 'closed'))
```

### `order_items`

| Column | Contract |
|---|---|
| `id` | generated identity primary key |
| `order_id` | required reference to `orders(id)` |
| `book_id` | required reference to `books(id)` |
| `quantity` | required integer greater than zero |
| `unit_price_paise` | required integer, zero or greater |

One book may appear at most once in the same order. Enforce that rule with a
named composite unique constraint called `unique_order_book`.

## Fixed Input

Insert rows in dependency order so the generated IDs have the values shown.

### Authors

```text
Ursula Le Guin
Octavia Butler
```

### Books

```text
isbn|title|author_id|price_paise
978-1|A Wizard of Earthsea|1|49900
978-2|Kindred|2|59900
978-3|Parable of the Sower|2|69900
```

### Customers

```text
name|email
Maya|maya@example.com
Noah|noah@example.com
```

### Orders

```text
customer_id|status
1|paid
2|pending
```

### Order items

```text
order_id|book_id|quantity|unit_price_paise
1|1|1|49900
1|2|2|59900
2|3|1|69900
```

## Your Exercise

Replace the starter comment in `main.sql`.

1. Suppress expected drop notices.
2. Drop all five tables in a dependency-safe order so the file is rerunnable.
3. Create the five tables with every required constraint.
4. Insert exactly the fixed rows above.
5. Write one join query that travels through:

```text
orders → customers → order_items → books
```

6. Select exactly these aliases in this order:

```text
order_id, customer_email, book_title, quantity, unit_price_paise
```

7. Sort by order ID and then book ID, both ascending.

Stop after this report. Do not add transactions, indexes, prepared statements,
or SQLC annotations yet; later stages will add them to this schema.

## Expected Output

Running `main.sql` must print exactly:

```text
order_id|customer_email|book_title|quantity|unit_price_paise
1|maya@example.com|A Wizard of Earthsea|1|49900
1|maya@example.com|Kindred|2|59900
2|noah@example.com|Parable of the Sower|1|69900
```

## Verify

From `databases`, run:

```bash
docker compose exec -T postgres psql -X -q \
  --username course_user --dbname sql_course \
  --set ON_ERROR_STOP=1 \
  --set QUIET=on \
  --pset format=unaligned \
  --pset 'fieldsep=|' \
  --pset tuples_only=off \
  --pset footer=off \
  --file main.sql
```

Run it twice. Both runs must produce the same output, then say `done`.

## Acceptance Criteria

- The file succeeds twice without manual cleanup.
- The schema contains exactly the required five tables and columns.
- Primary keys, foreign keys, uniqueness, nullability, and checks match the
  contract.
- `unique_order_book` protects the `(order_id, book_id)` pair.
- Seed data matches the fixed input exactly.
- The report uses four tables and prints the exact expected rows and columns.
- No later-stage transaction, index, prepared-query, or SQLC work is included.
