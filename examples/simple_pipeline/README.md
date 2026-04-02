# Simple Pipeline — Everything in One Python File

**Before cloud orchestration, before Airflow, before Bronze/Silver/Gold — this is where every data pipeline starts.**

---

## What This Demonstrates

Two complete pipelines, each in a single Python file:

1. **`analytics_pipeline.py`** — Loads raw call center data, cleans it, builds a star schema, runs analytical queries. The DE (Data Engineering) pipeline.
2. **`ml_pipeline.py`** — Loads the same data, engineers features, trains models, evaluates, explains with SHAP. The ML (Machine Learning) pipeline.

Both run locally. No cloud. No Docker. No Airflow. Just `python analytics_pipeline.py` and see results.

**Then:** [Why This Breaks at Scale](#why-this-breaks-at-scale) — and why cloud pipelines (GCS, BigQuery, Dataflow, Cloud Composer) exist.

---

## How to Run

```bash
# Setup
pip install pandas numpy scikit-learn shap matplotlib seaborn

# Run the analytics pipeline (DE)
python analytics_pipeline.py

# Run the ML pipeline (AI/ML)
python ml_pipeline.py
```

Both scripts use the call center data from the `data/` directory in this repo. If the data files are not in the expected path, update the `DATA_DIR` variable at the top of each script.

---

## Why This Breaks at Scale

These single-file pipelines work for 510 calls. They break when:

| Problem | At 510 Rows | At 50 Million Rows |
|:---|:---|:---|
| **Memory** | Fits in RAM easily | Pandas loads everything into memory — machine crashes or swaps to disk |
| **Speed** | Runs in 2 seconds | Runs in 4 hours — if it finishes at all |
| **Scheduling** | Run manually when needed | Must run every night at 2 AM without human intervention |
| **Failure recovery** | If it crashes, re-run from the top | If step 7 of 12 fails, must restart from step 7 — not step 1 |
| **Data freshness** | One-time analysis | New data arrives every hour — the pipeline must run continuously |
| **Multiple consumers** | One analyst, one notebook | Analytics team needs the star schema, ML team needs clean features, both from the same source |
| **Audit trail** | "I ran the script" | "Which version of the code processed which data at what time with what result?" |
| **Team collaboration** | One person | Five engineers working on different pipeline steps simultaneously |

**That is why cloud pipelines exist:**

| Single-File Pipeline | Cloud Pipeline |
|:---|:---|
| `pandas.read_csv()` in memory | GCS (Google Cloud Storage) → BigQuery (processes terabytes without loading into memory) |
| All steps in one script | Each step is a separate task in Airflow/Cloud Composer — can fail and retry independently |
| Run manually | Scheduled (cron) or triggered (new file lands in GCS → pipeline starts) |
| No history | Every run logged: what data, what code version, what output, when |
| One machine | Distributed across many machines (Dataflow/Dataproc scale horizontally) |

**The single-file pipeline is not wrong.** It is where every pipeline starts. The cloud version is where it goes when the data grows, the team grows, and the stakes grow. Understanding both is what separates a practitioner who builds from one who only operates.
