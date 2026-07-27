INSERT INTO products (price_paise)
VALUES (1000);

INSERT INTO products (name, price_paise, available)
VALUES ('Broken Price', -1, TRUE);

INSERT INTO products (name, price_paise, available)
VALUES ('Broken Availability', 1000, 2);

INSERT INTO products (name, price_paise, available)
VALUES ('Raagi Malt', 5000, TRUE);

SELECT * FROM products;
