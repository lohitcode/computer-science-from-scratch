# Checkpoint 13: Normalize a Relational Schema

Status: **Complete**

## Goal

Learn how to:

- find facts that are repeated in a table;
- recognize update, insert, and delete anomalies;
- separate facts according to what they describe;
- use primary and foreign keys to reconnect normalized data;
- follow a relationship chain by joining more than two tables.

This lesson is about **designing the tables**. You already know the SQL needed
to create them and read the final result.

## Why Normalization Exists

Early data systems often stored whole records together because that matched a
paper form or report. The relational model changed the question from “what
does this screen look like?” to:

> What facts exist, and what uniquely determines each fact?

Suppose a bookstore starts with this table:

```text
sale_id|customer_email|customer_name|book_isbn|book_title|quantity
1|maya@example.com|Maya|978-1|Dune|1
2|maya@example.com|Maya|978-2|Kindred|2
3|noah@example.com|Noah|978-1|Dune|1
```

It looks convenient, but customer and book facts are repeated.

### Update anomaly

If Maya changes her name, every row containing her email must be updated. If
one is missed, the database claims that one email belongs to two names.

### Insert anomaly

You cannot store a new book until somebody buys it, unless sale columns are
allowed to contain meaningless values.

### Delete anomaly

Deleting Noah's only sale might also delete the only stored copy of a fact
about Noah.

These are not merely storage inefficiencies. They allow one real-world fact to
develop conflicting copies.

## The Core Question: What Does This Fact Describe?

Ask what identifier determines each value:

```text
customer email → customer name
book ISBN      → book title
sale ID        → which customer made the sale
sale + book    → quantity bought
```

The arrow means “determines.” If an email identifies one customer, knowing the
email determines that customer's name. This relationship is called a
**functional dependency**.

A useful design rule follows:

> Store a fact with the key that determines it.

That produces separate customer, book, sale, and sale-item relations. Foreign
keys reconnect them when a query needs the report-shaped view.

## Practical Meaning of 1NF, 2NF, and 3NF

The normal forms are stages for detecting misplaced facts.

### First normal form: one value per cell

Do not store a list such as this:

```text
sale_id|book_isbns
1|978-1,978-2
```

The database cannot reliably constrain, join, or count individual ISBNs in
that text. Store one sale-book relationship per row instead.

### Second normal form: depend on the whole key

Imagine a sale-items table identified by `(sale_id, book_isbn)`:

```text
sale_id|book_isbn|book_title|quantity
```

`quantity` describes that particular book in that particular sale, so it
depends on the whole key. `book_title` depends only on `book_isbn`, so it
belongs with the book—not in the sale item.

This issue matters when a table has a multi-column key.

### Third normal form: non-key facts should not determine other non-key facts

Consider:

```text
sale_id|customer_id|customer_email
```

The sale ID determines the customer ID, but the customer ID determines the
email. The email is a customer fact stored indirectly in a sale row. Keep only
`customer_id` in the sale and obtain the email by joining the customer table.

For ordinary application schemas, this practical summary gets you far:

```text
1NF → one value per cell, one kind of row
2NF → every non-key fact depends on the entire key
3NF → non-key facts do not describe other non-key facts
```

## Normalization Is Not “Never Duplicate a Value”

Repeated foreign-key values are expected. Ten orders can contain the same
`customer_id`; those values express ten relationships.

Some duplication can also be intentional. For example, an order item may
store the price charged at checkout even though a product has a current price.
Those are different facts:

```text
products.current_price  → price now
order_items.unit_price  → price agreed for that sale
```

Normalization is about avoiding multiple uncontrolled copies of the **same
fact**, not mechanically eliminating every repeated value.

## Joining More Than Two Tables

A query can contain multiple joins. Each new `JOIN` takes the result built so
far and connects one additional table.

Suppose a library has this relationship chain:

```text
members ← loans → books → authors
```

The arrows represent foreign keys:

```text
loans.member_id → members.id
loans.book_id   → books.id
books.author_id → authors.id
```

Start from the table representing the rows you want—in this case, loans—and
follow one relationship at a time:

```sql
SELECT
    l.id AS loan_id,
    m.name AS member_name,
    b.title AS book_title,
    a.name AS author_name
FROM loans AS l
JOIN members AS m
    ON m.id = l.member_id
JOIN books AS b
    ON b.id = l.book_id
JOIN authors AS a
    ON a.id = b.author_id
ORDER BY l.id;
```

`JOIN` here means `INNER JOIN`; the two spellings are equivalent. The query is
not one special “four-table join.” It is a sequence:

```text
1. Start with loans.
2. Attach the matching member to each loan.
3. Attach the matching book to each surviving row.
4. Attach the matching author to each surviving row.
```

After a table has been introduced by `FROM` or `JOIN`, its alias is available
to later `ON` conditions. That is why the final join can use `b.author_id`:
`books AS b` was introduced immediately before it.

Every join needs its own relationship condition. Writing several joins does
not make PostgreSQL infer foreign-key paths automatically.

With inner joins, a row disappears if any required link in the chain has no
match. When one relationship is optional, that particular step may instead
need `LEFT JOIN`, using the behavior from Lesson 12.

## Your Exercise

Replace the current product/category exercise in `main.sql` with a normalized
order schema. Do not copy the bookstore example's table design; model the
following business facts yourself using the required contract.

### Fixed input

The unnormalized information is:

```text
order_id|customer_name|customer_email|product_name|price_paise|quantity
1|Asha|asha@example.com|Raagi Malt|5000|2
1|Asha|asha@example.com|Sprout Salad|6500|1
2|Ravi|ravi@example.com|Fruit Juice|8000|3
```

### Required normalized model

Create these four tables and give each fact only one authoritative home:

- `customers`: customer identity, name, and email;
- `products`: product identity, name, and current price;
- `orders`: order identity and the customer who owns it;
- `order_items`: the products and quantities belonging to each order.

Your schema must enforce these business rules:

- customer emails are unique and required;
- product names are unique and required;
- prices cannot be negative;
- every order references an existing customer;
- every order item references an existing order and product;
- quantity must be greater than zero;
- a product may appear at most once in the same order.

Use generated integer identity keys for customers and products. Use the fixed
order IDs `1` and `2` so the expected result is deterministic. Choose an
appropriate key for `order_items` based on its business identity.

Insert the fixed input without repeating customer names, customer emails,
product names, or current prices in `orders` or `order_items`.

### Result query

Write one query that reconstructs the order details by joining all four
tables. Return exactly these aliases in this order:

```text
order_id, customer_name, product_name, price_paise, quantity
```

Order the result by order ID and then product ID.

## Expected Output

```text
order_id|customer_name|product_name|price_paise|quantity
1|Asha|Raagi Malt|5000|2
1|Asha|Sprout Salad|6500|1
2|Ravi|Fruit Juice|8000|3
```

## Run and Verify

From `databases`, enter `psql`:

```bash
docker compose exec postgres \
  psql --username course_user --dbname sql_course
```

Run the file twice:

```text
\i main.sql
\i main.sql
```

Both runs must produce the exact expected output. Rerunnability requires you
to drop dependent tables before the tables they reference.

You can inspect your design with:

```text
\dt
\d customers
\d products
\d orders
\d order_items
```

## Acceptance Criteria

- The schema has exactly the four required tables.
- Each descriptive fact has one authoritative table.
- Lists are not stored inside a text column.
- Primary, unique, check, and foreign-key constraints enforce every stated
  business rule.
- Customer or product descriptive fields are not copied into `orders` or
  `order_items`.
- The result is reconstructed with joins and exactly matches the expected
  output on two consecutive runs.
- `invalid.sql` is unchanged in this checkpoint.

## Think Before You Write

Before writing SQL, answer these on paper or in your head:

1. What real-world thing does one row in each table represent?
2. What uniquely identifies that row?
3. Which key determines each non-key column?
4. Which table must be created first, and which must be dropped first?

If those answers are clear, the DDL becomes a translation of your model.

## Stop Here

Say `done` when both runs match. Do not start transactions yet.
