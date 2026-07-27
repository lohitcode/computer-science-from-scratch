# Checkpoint 04: Filter Rows

Status: **Complete**

## Goal

Use `WHERE` with comparisons, `AND`, `OR`, and `NOT`.

## Starting Rows

| `id` | `name` | `price_paise` | `available` |
|---:|---|---:|---|
| 1 | Raagi Malt | 5000 | `TRUE` |
| 2 | Fruit Juice | 8000 | `TRUE` |
| 3 | Sprout Salad | 6500 | `FALSE` |

## Completed Contract

Every query selects only `name`:

1. Availability equals `TRUE`.
2. Price is at least `6000`.
3. Availability equals `TRUE` **and** price is below `6000`.
4. Name is `Fruit Juice` **or** `Sprout Salad`.
5. It is **not true** that availability equals `TRUE`.

## Completed Output

```text
name
Raagi Malt
Fruit Juice
name
Fruit Juice
Sprout Salad
name
Raagi Malt
name
Fruit Juice
Sprout Salad
name
Sprout Salad
```

Without `ORDER BY`, row order is not guaranteed. This checkpoint verifies the
logical result sets.

## Mental Model

```text
FROM products             choose source rows
WHERE price_paise >= 6000 keep matching rows
SELECT name               return this column
```

SQL equality uses `=`, not Go's `==`.
