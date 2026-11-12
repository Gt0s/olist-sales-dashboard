# DAX measures

All measures live in the `orders` table unless noted.

## Calendar table

Modeling → New table:

```DAX
Calendar =
ADDCOLUMNS (
    CALENDAR ( DATE ( 2017, 1, 1 ), DATE ( 2018, 8, 31 ) ),
    "Year", YEAR ( [Date] ),
    "Month", FORMAT ( [Date], "MMM yyyy" ),
    "MonthNo", YEAR ( [Date] ) * 100 + MONTH ( [Date] )
)
```

Sort the `Month` column by `MonthNo`, mark the table as a date table, and relate `Calendar[Date]` → `orders[order_date]` (one-to-many).

## Sales

```DAX
Revenue = SUM ( orders[revenue] )

Orders = DISTINCTCOUNT ( orders[order_id] )

Avg Order Value = DIVIDE ( [Revenue], [Orders] )

Customers = DISTINCTCOUNT ( orders[customer_unique_id] )

Revenue MoM % =
VAR prev = CALCULATE ( [Revenue], DATEADD ( Calendar[Date], -1, MONTH ) )
RETURN DIVIDE ( [Revenue] - prev, prev )
```

## Delivery & satisfaction

```DAX
Delivered Orders =
CALCULATE ( [Orders], orders[order_status] = "delivered" )

Late Orders =
CALCULATE ( [Orders], orders[order_status] = "delivered", orders[late] = TRUE () )

Late Delivery % = DIVIDE ( [Late Orders], [Delivered Orders] )

Avg Delivery Days =
CALCULATE ( AVERAGE ( orders[delivery_days] ), orders[order_status] = "delivered" )

Avg Review Score = AVERAGE ( orders[review_score] )
```

## Products (order_items table)

```DAX
Items Sold = COUNTROWS ( order_items )

Avg Item Price = AVERAGE ( order_items[price] )
```
