-- Checkpoint 18A: build the bookstore schema and report described in
-- lessons/18a-final-checkpoint-schema.md.
SET client_min_messages TO WARNING;

DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS books;
DROP TABLE IF EXISTS authors;

CREATE TABLE authors (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE books (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    isbn TEXT NOT NULL UNIQUE,
    title TEXT NOT NULL,
    author_id INTEGER NOT NULL REFERENCES authors(id),
    price_paise INTEGER NOT NULL CHECK (price_paise >=0)
);

CREATE TABLE customers (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE
);

CREATE TABLE orders (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customers(id),
    status TEXT NOT NULL CHECK( status IN ('pending', 'paid', 'cancelled'))
);

CREATE TABLE order_items(
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    order_id INTEGER NOT NULL REFERENCES orders(id),
    book_id INTEGER NOT NULL REFERENCES books(id),
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    unit_price_paise INTEGER NOT NULL CHECK (unit_price_paise >= 0),

    CONSTRAINT unique_order_book UNIQUE (order_id, book_id)
);

INSERT INTO authors (name)
VALUES
    ('Ursula Le Guin'),
    ('Octavia Butler');

INSERT INTO books (isbn, title, author_id, price_paise)
VALUES
    ('978-1','A Wizard of Earthsea',1,49900),
    ('978-2','Kindred',2,59900),
    ('978-3','Parable of the Sower',2,69900);

INSERT INTO customers (name, email)
VALUES
    ('Maya','maya@example.com'),
    ('Noah','noah@example.com');

INSERT INTO orders (customer_id, status)
VALUES
    (1, 'paid'),
    (2, 'pending');

INSERT INTO order_items (order_id, book_id, quantity, unit_price_paise)
VALUES
    (1,1,1,49900),
    (1,2,2,59900),
    (2,3,1,69900);



CREATE INDEX idx_orders_customer_id
ON orders (customer_id);

ANAlYZE orders;

SELECT indexname, indexdef
FROM pg_indexes
WHERE schemaname = 'public'
  AND tablename = 'orders'
  AND indexname = 'idx_orders_customer_id';


EXPLAIN (COSTS OFF)
SELECT id, customer_id, status
FROM orders
WHERE customer_id = 2;
