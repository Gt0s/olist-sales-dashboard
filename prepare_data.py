"""Clean the Olist e-commerce data and export tables ready for Power BI.

Run:  python prepare_data.py
Raw CSVs are read from data/raw/ (downloaded automatically from Olist's
public GitHub repository if they are missing). Clean tables are written
to data/processed/.
"""
from __future__ import annotations

from pathlib import Path
from urllib.request import urlretrieve

import pandas as pd

ROOT = Path(__file__).parent
RAW = ROOT / "data" / "raw"
OUT = ROOT / "data" / "processed"
SOURCE = "https://raw.githubusercontent.com/olist/work-at-olist-data/master/datasets/"
FILES = [
    "olist_orders_dataset.csv",
    "olist_order_items_dataset.csv",
    "olist_customers_dataset.csv",
    "olist_products_dataset.csv",
    "olist_order_reviews_dataset.csv",
    "olist_order_payments_dataset.csv",
    "product_category_name_translation.csv",
]


def ensure_raw() -> None:
    RAW.mkdir(parents=True, exist_ok=True)
    for name in FILES:
        path = RAW / name
        if not path.exists():
            print(f"Downloading {name} ...")
            urlretrieve(SOURCE + name, path)


def read(name: str, **kw) -> pd.DataFrame:
    return pd.read_csv(RAW / f"{name}.csv", **kw)


def build() -> tuple[pd.DataFrame, pd.DataFrame]:
    dates = ["order_purchase_timestamp", "order_delivered_customer_date",
             "order_estimated_delivery_date"]
    orders = read("olist_orders_dataset", parse_dates=dates)
    customers = read("olist_customers_dataset")
    items = read("olist_order_items_dataset")
    products = read("olist_products_dataset")
    reviews = read("olist_order_reviews_dataset")
    payments = read("olist_order_payments_dataset")
    translation = read("product_category_name_translation")

    # Keep only full months: the data starts in Sep 2016 and the last
    # weeks of 2018 have almost no orders.
    orders = orders[(orders["order_purchase_timestamp"] >= "2017-01-01")
                    & (orders["order_purchase_timestamp"] < "2018-09-01")]

    # Product category in English; missing categories become "unknown".
    products = products.merge(translation, on="product_category_name", how="left")
    products["category"] = (products["product_category_name_english"]
                            .fillna("unknown").str.replace("_", " "))

    # One review score per order (a few orders have several reviews: keep the latest).
    reviews = (reviews.sort_values("review_answer_timestamp")
               .drop_duplicates("order_id", keep="last")[["order_id", "review_score"]])

    # Main payment type per order = the one with the largest amount.
    main_payment = (payments.sort_values("payment_value")
                    .drop_duplicates("order_id", keep="last")[["order_id", "payment_type"]])
    main_payment["payment_type"] = main_payment["payment_type"].str.replace("_", " ")

    # Item-level table.
    order_items = (items.merge(products[["product_id", "category"]], on="product_id", how="left")
                   .loc[lambda d: d["order_id"].isin(orders["order_id"])]
                   [["order_id", "order_item_id", "product_id", "seller_id",
                     "category", "price", "freight_value"]])

    # Order-level table.
    totals = (order_items.groupby("order_id")
              .agg(items=("order_item_id", "count"), revenue=("price", "sum"),
                   freight=("freight_value", "sum"))
              .reset_index())
    o = (orders.merge(customers[["customer_id", "customer_unique_id", "customer_state",
                                 "customer_city"]], on="customer_id", how="left")
         .merge(totals, on="order_id", how="left")
         .merge(reviews, on="order_id", how="left")
         .merge(main_payment, on="order_id", how="left"))

    delivered = o["order_delivered_customer_date"].notna()
    o["delivery_days"] = (o["order_delivered_customer_date"]
                          - o["order_purchase_timestamp"]).dt.days.where(delivered)
    o["late"] = (o["order_delivered_customer_date"].dt.normalize()
                 > o["order_estimated_delivery_date"].dt.normalize()).where(delivered)
    o["order_date"] = o["order_purchase_timestamp"].dt.date
    o["customer_city"] = o["customer_city"].str.title()

    o = o[["order_id", "customer_unique_id", "order_date", "order_status",
           "customer_state", "customer_city", "items", "revenue", "freight",
           "payment_type", "review_score", "delivery_days", "late"]]
    return o, order_items


def main() -> None:
    ensure_raw()
    orders, order_items = build()
    OUT.mkdir(parents=True, exist_ok=True)
    orders.to_csv(OUT / "orders.csv", index=False)
    order_items.to_csv(OUT / "order_items.csv", index=False)
    print(f"orders.csv: {len(orders):,} rows | order_items.csv: {len(order_items):,} rows")


if __name__ == "__main__":
    main()
