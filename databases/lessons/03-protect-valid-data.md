# Checkpoint 03: Protect Valid Data

Status: **Complete**

## Goal

Use PostgreSQL types and constraints to reject invalid names, prices, and
availability values.

## Completed Schema

| Column | PostgreSQL definition |
|---|---|
| `id` | Generated integer primary key |
| `name` | Required, unique text |
| `price_paise` | Required non-negative integer |
| `available` | Required boolean, default `TRUE` |

Fixed valid rows:

| `name` | `price_paise` | `available` |
|---|---:|---|
| Raagi Malt | 5000 | Omitted to test `TRUE` default |
| Fruit Juice | 8000 | `TRUE` |
| Sprout Salad | 6500 | `FALSE` |

## Completed Output

PostgreSQL displays boolean values as `t` and `f` in unaligned output:

```text
1|Raagi Malt|5000|t
2|Fruit Juice|8000|t
3|Sprout Salad|6500|f
```

## Invalid Checks

`invalid.sql` attempts:

| Test | Invalid input | Protection |
|---|---|---|
| Missing name | Omit `name` | `NOT NULL` |
| Negative price | Price `-1` | `CHECK` |
| Invalid availability | Integer `2` | `BOOLEAN` type |
| Duplicate name | Another `Raagi Malt` | `UNIQUE` |

All four inserts fail, and the final table remains unchanged.

```text
application validation → friendly caller error
database constraint    → final stored-data protection
```
