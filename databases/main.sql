SET client_min_messages TO WARNING;


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

SELECT
    oi.order_id,
    c.name AS customer_name,
    p.name AS product_name,
    oi.unit_price_paise AS price_paise,
    oi.quantity
FROM orders o
JOIN customers c ON o.customer_id =  c.id
JOIN order_items oi ON o.id = oi.order_id
JOIN products p ON oi.product_id = p.id
ORDER BY o.id, p.id;
