"""
Analytics Pipeline — Everything in One Python File
===================================================

Loads raw call center data → cleans it → builds a star schema → runs analytical queries.

This is the Data Engineering pipeline in its simplest form.
No cloud. No orchestration. Just Python + Pandas.

Run: python3 analytics_pipeline.py
"""

import pandas as pd
import numpy as np
import os

# ============================================================
# CONFIG — Change this to point to your data directory
# ============================================================
DATA_DIR = os.path.expanduser("~/Downloads/data-engineer-accelerator/data")

print("=" * 70)
print("ANALYTICS PIPELINE — Call Center Data")
print("=" * 70)

# ============================================================
# STAGE 1: BRONZE — Load raw data exactly as it arrived
# ============================================================
# Bronze = raw, untouched. Every record preserved. No cleaning.
# WHY: This is the source of truth. If anything goes wrong downstream,
# we can always come back here and reprocess from scratch.

print("\n[BRONZE] Loading raw data...")

calls_raw = pd.read_json(os.path.join(DATA_DIR, "calls.json"), lines=True)
campaigns_raw = pd.read_csv(os.path.join(DATA_DIR, "campaigns.csv"))
products_raw = pd.read_csv(os.path.join(DATA_DIR, "products.csv"))
orders_raw = pd.read_csv(os.path.join(DATA_DIR, "orders.csv"))

print(f"  calls:     {len(calls_raw):,} records, columns: {list(calls_raw.columns)}")
print(f"  campaigns: {len(campaigns_raw):,} records")
print(f"  products:  {len(products_raw):,} records")
print(f"  orders:    {len(orders_raw):,} records")

# ============================================================
# STAGE 2: SILVER — Clean the data (but keep ALL records)
# ============================================================
# Silver = cleaned but complete. Duplicates removed, types fixed.
# Missing values FLAGGED, not dropped.
# WHY: Analytics needs every record for accurate counts.

print("\n[SILVER] Cleaning data...")

calls = calls_raw.copy()

# --- Flatten nested customer data ---
# WHY: The JSON has a nested "customer" object. Flatten it for SQL-like queries.
if "customer" in calls.columns:
    customer_df = pd.json_normalize(calls["customer"])
    customer_df.columns = ["customer_" + c.replace(".", "_") for c in customer_df.columns]
    calls = pd.concat([calls.drop(columns=["customer"]), customer_df], axis=1)

# --- Deduplicate ---
dupes_before = len(calls)
calls = calls.drop_duplicates(subset=["call_id"], keep="first")
dupes_removed = dupes_before - len(calls)
print(f"  Duplicates removed: {dupes_removed}")

# --- Fix data types ---
calls["date"] = pd.to_datetime(calls["date"], errors="coerce")
calls["start_time"] = pd.to_datetime(calls["start_time"], errors="coerce", utc=True)
calls["end_time"] = pd.to_datetime(calls["end_time"], errors="coerce", utc=True)
calls["dnis"] = calls["dnis"].astype(str)

# --- Standardize text ---
calls["disposition"] = calls["disposition"].str.strip().str.lower()
calls["channel"] = calls["channel"].str.strip().str.upper()

# --- Flag missing values (do NOT drop them) ---
for col in ["duration", "disposition", "start_time"]:
    flag_col = f"has_missing_{col}"
    calls[flag_col] = calls[col].isna()
    missing_count = calls[flag_col].sum()
    if missing_count > 0:
        print(f"  Missing '{col}': {missing_count} records (flagged, not dropped)")

print(f"  Silver calls: {len(calls):,} records (all preserved)")

# ============================================================
# STAGE 3: GOLD (Analytics) — Build the star schema
# ============================================================
# Dimension tables + fact table. Surrogate keys for fast joins.
# WHY: Makes analytical queries simple and fast.

print("\n[GOLD] Building star schema...")

# --- Dimension: dim_date ---
unique_dates = calls["date"].dropna().dt.date.unique()
dim_date = pd.DataFrame({"full_date": sorted(unique_dates)})
dim_date["date_key"] = range(1, len(dim_date) + 1)
dim_date["full_date"] = pd.to_datetime(dim_date["full_date"])
dim_date["day_name"] = dim_date["full_date"].dt.day_name()
dim_date["month_name"] = dim_date["full_date"].dt.month_name()
dim_date["is_weekend"] = dim_date["full_date"].dt.dayofweek >= 5
print(f"  dim_date: {len(dim_date)} rows")

# --- Dimension: dim_campaign ---
campaigns = campaigns_raw.copy()
campaigns["dnis"] = campaigns["dnis"].astype(str)
campaigns["campaign_key"] = range(1, len(campaigns) + 1)
dim_campaign = campaigns
print(f"  dim_campaign: {len(dim_campaign)} rows")

# --- Dimension: dim_product ---
products = products_raw.copy()
products["product_key"] = range(1, len(products) + 1)
dim_product = products
print(f"  dim_product: {len(dim_product)} rows")

# --- Fact table: fact_calls ---
fact_calls = calls.copy()

# Join campaign key
fact_calls = fact_calls.merge(
    dim_campaign[["dnis", "campaign_key", "campaign_name", "channel"]].rename(
        columns={"channel": "campaign_channel"}),
    on="dnis", how="left"
)

# Join date key
fact_calls["date_str"] = fact_calls["date"].dt.date.astype(str)
dim_date["date_str"] = dim_date["full_date"].dt.date.astype(str)
fact_calls = fact_calls.merge(dim_date[["date_str", "date_key"]], on="date_str", how="left")
fact_calls.drop(columns=["date_str"], inplace=True)
dim_date.drop(columns=["date_str"], inplace=True)

# Extract hour for time-of-day analysis
if "start_time" in fact_calls.columns:
    fact_calls["hour_of_day"] = fact_calls["start_time"].dt.hour
    fact_calls["time_period"] = pd.cut(
        fact_calls["hour_of_day"],
        bins=[-1, 5, 11, 17, 21, 24],
        labels=["Night", "Morning", "Afternoon", "Evening", "Night_Late"]
    )

print(f"  fact_calls: {len(fact_calls):,} rows")

# ============================================================
# STAGE 4: ANALYTICAL QUERIES — The payoff
# ============================================================

print("\n[QUERIES] Running analytical queries...")
print("-" * 70)

# Query 1: Average call duration by campaign
result1 = fact_calls.groupby(["campaign_name", "campaign_channel"]).agg(
    avg_duration=("duration", "mean"),
    total_calls=("call_id", "count")
).round(1).sort_values("avg_duration", ascending=False)

print("\nQuery 1: Average call duration by campaign")
print(result1.to_string())

# Query 2: Calls by day of week
q2 = fact_calls.merge(dim_date[["date_key", "day_name", "is_weekend"]], on="date_key", how="left")
result2 = q2.groupby(["day_name", "is_weekend"]).agg(
    total_calls=("call_id", "count")
).sort_values("total_calls", ascending=False)

print("\n\nQuery 2: Calls by day of week")
print(result2.to_string())

# Query 3: Disposition (outcome) distribution
result3 = fact_calls["disposition"].value_counts()
print("\n\nQuery 3: Call disposition distribution")
print(result3.to_string())

# Query 4: Channel distribution (VA vs Live)
result4 = fact_calls.groupby("campaign_channel").agg(
    total_calls=("call_id", "count"),
    avg_duration=("duration", "mean")
).round(1)
print("\n\nQuery 4: Channel distribution (VA vs Live)")
print(result4.to_string())

# Query 5: Calls by time of day
if "time_period" in fact_calls.columns:
    result5 = fact_calls["time_period"].value_counts().sort_index()
    print("\n\nQuery 5: Calls by time of day")
    print(result5.to_string())

# Query 6: Data quality report
print("\n\nQuery 6: Data quality report")
missing_cols = [c for c in fact_calls.columns if c.startswith("has_missing_")]
for col in missing_cols:
    field = col.replace("has_missing_", "")
    missing = fact_calls[col].sum()
    total = len(fact_calls)
    pct = 100.0 * missing / total
    print(f"  {field}: {missing}/{total} missing ({pct:.1f}%)")

print("\n" + "=" * 70)
print("ANALYTICS PIPELINE COMPLETE")
print(f"Bronze: {len(calls_raw):,} raw records")
print(f"Silver: {len(calls):,} cleaned records (all preserved)")
print(f"Gold:   {len(fact_calls):,} fact rows | {len(dim_date)} dates | {len(dim_campaign)} campaigns | {len(dim_product)} products")
print("=" * 70)
