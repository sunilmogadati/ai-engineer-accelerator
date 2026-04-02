"""
ML Pipeline — Everything in One Python File
============================================

Loads call center data → cleans → engineers features → trains models →
evaluates → explains with SHAP.

This is the Machine Learning pipeline in its simplest form.
No cloud. No MLflow. Just Python + scikit-learn.

Run: python3 ml_pipeline.py
"""

import pandas as pd
import numpy as np
import os
import warnings
warnings.filterwarnings("ignore")

# ============================================================
# CONFIG
# ============================================================
DATA_DIR = os.path.expanduser("~/Downloads/data-engineer-accelerator/data")

print("=" * 70)
print("ML PIPELINE — Call Center Churn Risk Prediction")
print("=" * 70)

# ============================================================
# STAGE 1: BRONZE — Load raw data
# ============================================================

print("\n[BRONZE] Loading raw data...")

calls_raw = pd.read_json(os.path.join(DATA_DIR, "calls.json"), lines=True)
campaigns_raw = pd.read_csv(os.path.join(DATA_DIR, "campaigns.csv"))
orders_raw = pd.read_csv(os.path.join(DATA_DIR, "orders.csv"))

print(f"  calls:     {len(calls_raw):,} records")
print(f"  campaigns: {len(campaigns_raw):,} records")
print(f"  orders:    {len(orders_raw):,} records")

# ============================================================
# STAGE 2: SILVER — Clean the data
# ============================================================

print("\n[SILVER] Cleaning data...")

calls = calls_raw.copy()

# Flatten nested customer data
if "customer" in calls.columns:
    customer_df = pd.json_normalize(calls["customer"])
    customer_df.columns = ["customer_" + c.replace(".", "_") for c in customer_df.columns]
    calls = pd.concat([calls.drop(columns=["customer"]), customer_df], axis=1)

# Deduplicate
calls = calls.drop_duplicates(subset=["call_id"], keep="first")

# Fix types
calls["date"] = pd.to_datetime(calls["date"], errors="coerce")
calls["start_time"] = pd.to_datetime(calls["start_time"], errors="coerce", utc=True)
calls["end_time"] = pd.to_datetime(calls["end_time"], errors="coerce", utc=True)
calls["dnis"] = calls["dnis"].astype(str)
calls["disposition"] = calls["disposition"].str.strip().str.lower()
calls["channel"] = calls["channel"].str.strip().str.upper()

print(f"  Silver calls: {len(calls):,} records")

# ============================================================
# STAGE 3: GOLD (ML) — Filter for clean records + engineer features
# ============================================================
# Unlike analytics Gold (keeps ALL records), ML Gold DROPS records
# with missing values in critical feature columns.
# WHY: ML models cannot train on NULL.

print("\n[GOLD - ML] Engineering features...")

ml_data = calls.copy()

# --- Join campaign info ---
campaigns_raw["dnis"] = campaigns_raw["dnis"].astype(str)
ml_data = ml_data.merge(campaigns_raw[["dnis", "campaign_name", "client_name", "channel"]].rename(
    columns={"channel": "campaign_channel"}), on="dnis", how="left")

# --- Join order info ---
order_summary = orders_raw.groupby("call_id").agg(
    order_count=("order_id", "count"),
    total_revenue=("total", "sum")
).reset_index()
ml_data = ml_data.merge(order_summary, on="call_id", how="left")
ml_data["order_count"] = ml_data["order_count"].fillna(0).astype(int)
ml_data["total_revenue"] = ml_data["total_revenue"].fillna(0)
ml_data["placed_order"] = (ml_data["order_count"] > 0).astype(int)

# --- Traditional features ---
ml_data["hour_of_day"] = ml_data["start_time"].dt.hour
ml_data["is_weekend"] = (ml_data["start_time"].dt.dayofweek >= 5).astype(int)
ml_data["is_va"] = (ml_data["campaign_channel"] == "VA").astype(int)

# --- Target variable ---
# Churn risk proxy: callback, abandoned, or voicemail = unresolved = churn risk
# In production, actual churn data would come from CRM (Customer Relationship Management).
ml_data["is_churn_risk"] = ml_data["disposition"].isin(
    ["callback", "abandoned", "voicemail"]
).astype(int)

churn_rate = ml_data["is_churn_risk"].mean()
print(f"  Churn risk rate: {churn_rate:.1%} (simulated from dispositions)")
print(f"  Disposition breakdown:")
print(f"  {ml_data['disposition'].value_counts().to_dict()}")

# --- Drop nulls in critical features ---
critical = ["duration", "hour_of_day"]
before = len(ml_data)
ml_data = ml_data.dropna(subset=critical)
dropped = before - len(ml_data)
if dropped > 0:
    print(f"  Dropped {dropped} records with missing features")

print(f"  ML-ready records: {len(ml_data):,}")

# ============================================================
# STAGE 4: MODEL TRAINING & EVALUATION
# ============================================================

print("\n[MODEL] Training and evaluating...")

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, classification_report
)
from sklearn.preprocessing import StandardScaler

# Select features
feature_cols = ["duration", "hour_of_day", "is_weekend", "is_va",
                "placed_order", "order_count", "total_revenue"]

X = ml_data[feature_cols].fillna(0)
y = ml_data["is_churn_risk"]

print(f"  Features ({len(feature_cols)}): {feature_cols}")
print(f"  Target: is_churn_risk")
print(f"  Class balance: {dict(y.value_counts())}")

# Split (stratify keeps the class ratio the same in train and test)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
print(f"  Train: {len(X_train)} | Test: {len(X_test)}")

# Scale (Logistic Regression needs this, Random Forest does not, but it does not hurt)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train models
models = {
    "Logistic Regression": LogisticRegression(random_state=42, class_weight="balanced"),
    "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42, class_weight="balanced")
}

results = []

for name, model in models.items():
    if "Logistic" in name:
        model.fit(X_train_scaled, y_train)
        y_pred = model.predict(X_test_scaled)
        y_proba = model.predict_proba(X_test_scaled)[:, 1]
        cv_scores = cross_val_score(model, X_train_scaled, y_train, cv=5, scoring="f1")
    else:
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        y_proba = model.predict_proba(X_test)[:, 1]
        cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring="f1")

    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, zero_division=0)
    rec = recall_score(y_test, y_pred, zero_division=0)
    f1 = f1_score(y_test, y_pred, zero_division=0)
    auc = roc_auc_score(y_test, y_proba) if len(y_test.unique()) > 1 else 0

    results.append({"Model": name, "Accuracy": acc, "Precision": prec,
                     "Recall": rec, "F1": f1, "ROC-AUC": auc})

    print(f"\n  {name}:")
    print(f"    Accuracy:  {acc:.3f}")
    print(f"    Precision: {prec:.3f}  (of flagged churn risks, how many are real?)")
    print(f"    Recall:    {rec:.3f}  (of actual risks, how many caught?)")
    print(f"    F1:        {f1:.3f}")
    print(f"    ROC-AUC:   {auc:.3f}")
    print(f"    5-Fold CV: {cv_scores.mean():.3f} ± {cv_scores.std():.3f}")

# Comparison table
print("\n" + "-" * 70)
print("MODEL COMPARISON")
print("-" * 70)
results_df = pd.DataFrame(results).set_index("Model")
print(results_df.round(3).to_string())

# ============================================================
# STAGE 5: EXPLAINABILITY — SHAP
# ============================================================

print("\n[SHAP] Explaining predictions...")

try:
    import shap

    rf_model = models["Random Forest"]
    explainer = shap.TreeExplainer(rf_model)
    shap_values = explainer.shap_values(X_test)

    # Binary classification: shap_values may be [class_0, class_1] or a 3D array
    if isinstance(shap_values, list):
        shap_vals = shap_values[1]
    elif shap_values.ndim == 3:
        shap_vals = shap_values[:, :, 1]  # shape (n_samples, n_features, n_classes) → class 1
    else:
        shap_vals = shap_values

    # Feature importance
    importance = pd.DataFrame({
        "Feature": feature_cols,
        "Mean |SHAP|": np.abs(shap_vals).mean(axis=0)
    }).sort_values("Mean |SHAP|", ascending=False)

    print("\n  Feature Importance (SHAP — what drives churn risk predictions):")
    print("  " + "-" * 50)
    max_val = importance["Mean |SHAP|"].max()
    for _, row in importance.iterrows():
        bar_len = int(30 * row["Mean |SHAP|"] / max_val) if max_val > 0 else 0
        bar = "█" * bar_len
        print(f"  {row['Feature']:20s} {row['Mean |SHAP|']:.4f} {bar}")

    # Explain one prediction
    idx = 0
    pred = rf_model.predict(X_test.iloc[[idx]])[0]
    proba = rf_model.predict_proba(X_test.iloc[[idx]])[0][1]
    actual = y_test.iloc[idx]

    print(f"\n  Example prediction (test row {idx}):")
    print(f"    Predicted: {'CHURN RISK' if pred == 1 else 'NO RISK'} ({proba:.1%} probability)")
    print(f"    Actual:    {'CHURN RISK' if actual == 1 else 'NO RISK'}")
    print(f"    Why:")
    for feat, val, sv in zip(feature_cols, X_test.iloc[idx], shap_vals[idx]):
        direction = "↑ risk" if sv > 0 else "↓ risk"
        print(f"      {feat:20s} = {val:8.1f}  →  SHAP: {sv:+.4f} ({direction})")

except ImportError:
    print("  SHAP not installed. Run: pip install shap")

# ============================================================
# SUMMARY
# ============================================================
print("\n" + "=" * 70)
print("ML PIPELINE COMPLETE")
print(f"Bronze: {len(calls_raw):,} raw records")
print(f"Silver: {len(calls):,} cleaned records")
print(f"Gold (ML): {len(ml_data):,} feature-ready records")
print(f"Best model: {results_df['F1'].idxmax()} (F1: {results_df['F1'].max():.3f})")
print("=" * 70)
print()
print("WHY THIS BREAKS AT SCALE:")
print("  1. No scheduling    → Need Airflow/Cloud Composer for nightly runs")
print("  2. No versioning    → Need MLflow to track data + model + metrics")
print("  3. No serving       → Need FastAPI to serve predictions via API")
print("  4. No monitoring    → Need drift detection for silent degradation")
print("  5. No scale         → Pandas fails at 50M rows. Need BigQuery/Spark.")
print("  6. No separation    → Analytics and ML need different Gold views from same Silver")
print()
print("This script is the starting point. The cloud pipeline is the destination.")
