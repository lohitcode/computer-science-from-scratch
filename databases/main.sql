SET client_min_messages TO WARNING;

DROP TABLE IF EXISTS products;

CREATE TABLE products (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    price_paise INTEGER NOT NULL CHECK (price_paise >= 0),
    available BOOLEAN NOT NULL DEFAULT TRUE
);

INSERT INTO products (name, price_paise)
VALUES
    ('Raagi Malt', 5000);

INSERT INTO products (name, price_paise, available)
VALUES
    ('Fruit Juice', 8000, TRUE),
    ('Sprout Salad', 6500, FALSE);


SELECT name
FROM products
WHERE available = TRUE;

SELECT name
FROM products
WHERE price_paise >= 6000;

SELECT name
FROM products
WHERE available = TRUE AND price_paise < 6000;

SELECT name
FROM products
WHERE name = 'Fruit Juice' OR name = 'Sprout Salad';

SELECT name
FROM products
WHERE NOT (available = TRUE);
