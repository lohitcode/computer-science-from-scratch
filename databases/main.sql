DROP TABLE IF EXISTS products;

CREATE TABLE products (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    price_paise INTEGER NOT NULL CHECK (price_paise >= 0),
    available INTEGER NOT NULL DEFAULT 1 CHECK (available IN (0,1))
    );

INSERT INTO products (name, price_paise)
VALUES
    ('Raagi Malt', 5000);

INSERT INTO products (name, price_paise, available)
VALUES
    ('Fruit Juice', 8000, 1),
    ('Sprout Salad', 6500, 0);


SELECT * FROM products;
