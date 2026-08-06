-- name: GetCustomerByEmail :one
SELECT id, name, email
FROM customers
Where email = $1;

-- name: ListOrdersByCustomer :many
SELECT o.id AS order_id,
    c.email AS customer_email
FROM orders AS o
JOIN customers AS c
ON c.id =  o.customer_id
WHERE o.customer_id = $1
ORDER BY o.id;


-- name: UpdateOrderItemQuantity :one
UPDATE order_items
    SET quantity = $3
WHERE order_id = $1
    AND product_id = $2
RETURNING order_id, product_id, quantity;
