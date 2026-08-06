-- name: GetBookByISBN :one
SELECT id, isbn, title, price_paise
FROM books
WHERE isbn = $1;

-- name: ListOrderItems :many
SELECT oi.order_id AS order_id,
    b.title AS book_title,
    oi.quantity AS quantity,
    oi.unit_price_paise AS unit_price_paise
FROM order_items AS oi
JOIN books AS b
ON b.id =  oi.book_id
WHERE oi.order_id = $1
ORDER BY b.id ASC;


-- name: UpdateOrderItemQuantity :one
UPDATE order_items
    SET quantity = $3
WHERE order_id = $1
    AND book_id = $2
RETURNING order_id, book_id, quantity;
