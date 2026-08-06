SET client_min_messages TO WARNING;
DEALLOCATE ALL;

DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS products;


CREATE TABLE products (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    price_paise INTEGER NOT NULL CHECK (price_paise >= 0)
);

CREATE TABLE customers (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE
);

CREATE TABLE orders (
 id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
 customer_id INTEGER NOT NULL REFERENCES customers(id)
);

CREATE INDEX idx_orders_customer_id
ON orders (customer_id);

CREATE TABLE order_items (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    order_id INTEGER NOT NULL REFERENCES orders(id),
    product_id INTEGER NOT NULL REFERENCES products(id),
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    unit_price_paise INTEGER NOT NULL CHECK (unit_price_paise >= 0),

    CONSTRAINT unique_order_product UNIQUE (order_id, product_id)
);

INSERT INTO products (name, price_paise)
VALUES
    ('Raagi Malt', 5000),
    ('Sprout Salad', 6500),
    ('Fruit Juice', 8000);

INSERT INTO customers (name, email)
VALUES
    ('Asha', 'asha@example.com'),
    ('Ravi', 'ravi@example.com');

INSERT INTO orders (customer_id)
VALUES
    (1),
    (2);

INSERT INTO order_items (order_id, product_id, quantity, unit_price_paise)
VALUES
    (1, 1, 2, 5000),
    (1, 2, 1, 6500),
    (2, 3, 3, 8000);

PREPARE get_customer_by_email (TEXT) AS
SELECT id, name, email
FROM customers
WHERE email = $1;

EXECUTE get_customer_by_email('asha@example.com');


PREPARE list_orders_by_customer (INTEGER) AS
SELECT o.id AS order_id,
    c.email AS customer_email
FROM orders AS o
JOIN customers AS c
    ON c.id =  o.customer_id
WHERE o.customer_id = $1
ORDER BY o.id;

EXECUTE list_orders_by_customer(1);


PREPARE update_order_item_quantity (INTEGER, INTEGER, INTEGER) AS
UPDATE order_items
SET quantity = $3
WHERE order_id = $1 AND product_id = $2
RETURNING order_id, product_id, quantity;

EXECUTE update_order_item_quantity(1, 2, 3);
