SET client_min_messages TO WARNING;

DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS categories;

CREATE TABLE categories (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE products (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    price_paise INTEGER NOT NULL CHECK (price_paise >= 0),
    category_id INTEGER NOT NULL REFERENCES categories(id)
);

INSERT INTO categories (name)
VALUES
    ('Drinks'),
    ('Foods'),
    ('Desserts');

INSERT INTO products (name, price_paise, category_id)
VALUES
    ('Raagi Malt', 5000, 1),
    ('Fruit Juice', 8000, 1),
    ('Sprout Salad', 6500, 2);


SELECT
    c.name AS category_name,
    p.name AS product_name
FROM categories as c
LEFT JOIN products AS p
    ON p.category_id = c.id
ORDER BY c.id, p.id;


SELECT
    c.name AS category_name,
    COUNT(p.id) AS product_count,
    COALESCE(SUM(p.price_paise),0) AS total_price
FROM categories AS c
LEFT JOIN products AS p
    ON p.category_id = c.id
GROUP BY c.id, c.name
ORDER BY c.id;
