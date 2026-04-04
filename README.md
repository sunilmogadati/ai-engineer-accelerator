# AI Engineering Reference

**From ML fundamentals to production AI systems — concepts, code, and architecture.**

Building AI systems that work in production requires more than calling an API. It requires understanding the models behind the API, evaluating them honestly, explaining their predictions, and deploying them reliably.

This repository is a practitioner's reference for doing that — organized progressively from foundations to production.

---

## Concepts

Structured guides covering the WHY before the HOW. Each topic follows a consistent structure: why it matters → mental models → hello world → how it works → decisions → real-world architecture → system design → security → observability → checklist.

| Topic | Status | Start Here |
|:---|:---|:---|
| [**Deep Learning**](concepts/Deep_Learning/) | 10 chapters | [Why Deep Learning Matters](concepts/Deep_Learning/01_Why.md) |
| [**ML Fundamentals**](concepts/ML_Fundamentals/) | 4 chapters | [Why ML Engineering Matters](concepts/ML_Fundamentals/01_Why.md) |
| [**Data-to-Model Pipeline**](concepts/Data_to_Model_Pipeline.md) | Reference | The end-to-end flow from raw data to predictions |

---

## Notebooks

Hands-on Jupyter notebooks. Click any Colab badge to open and run — no local setup needed.

### Foundations

| Notebook | Open in Colab |
|:---|:---|
| [Python for AI](AI_Engineer_Accelerator_Python_for_AI.ipynb) | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/sunilmogadati/ai-engineer-accelerator/blob/main/AI_Engineer_Accelerator_Python_for_AI.ipynb) |
| [Python — Java Developer's Guide](Python_for_AI_Java_Dev_Guide.ipynb) | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/sunilmogadati/ai-engineer-accelerator/blob/main/Python_for_AI_Java_Dev_Guide.ipynb) |
| [Database Essentials](AI_Engineer_Accelerator_Database_Essentials.ipynb) — SQL, NoSQL, Vector DBs | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/sunilmogadati/ai-engineer-accelerator/blob/main/AI_Engineer_Accelerator_Database_Essentials.ipynb) |
| [Math for AI](AI_Engineer_Accelerator_Math_for_AI.ipynb) — linear algebra, calculus, probability | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/sunilmogadati/ai-engineer-accelerator/blob/main/AI_Engineer_Accelerator_Math_for_AI.ipynb) |

### Machine Learning

| Notebook | Open in Colab |
|:---|:---|
| [Linear Regression](Step1_Linear_Regression.ipynb) — the simplest ML model | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/sunilmogadati/ai-engineer-accelerator/blob/main/Step1_Linear_Regression.ipynb) |
| [Logistic Regression](Step2_Logistic_Regression.ipynb) — classification, precision/recall | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/sunilmogadati/ai-engineer-accelerator/blob/main/Step2_Logistic_Regression.ipynb) |
| [ML Fundamentals](AI_Engineer_Accelerator_ML_Fundamentals.ipynb) — bias-variance, regularization, SHAP, MLflow | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/sunilmogadati/ai-engineer-accelerator/blob/main/AI_Engineer_Accelerator_ML_Fundamentals.ipynb) |

### Deep Learning

| Notebook | Open in Colab |
|:---|:---|
| [Deep Learning & PyTorch](AI_Engineer_Accelerator_Deep_Learning_PyTorch.ipynb) — neural networks, training loops, diagnostics | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/sunilmogadati/ai-engineer-accelerator/blob/main/AI_Engineer_Accelerator_Deep_Learning_PyTorch.ipynb) |
| [CNN Deep Dive](AI_Engineer_Accelerator_Deep_Learning_CNN_DeepDive.ipynb) | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/sunilmogadati/ai-engineer-accelerator/blob/main/AI_Engineer_Accelerator_Deep_Learning_CNN_DeepDive.ipynb) |
| [Regularization](AI_Engineer_Accelerator_Deep_Learning_Regularization.ipynb) | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/sunilmogadati/ai-engineer-accelerator/blob/main/AI_Engineer_Accelerator_Deep_Learning_Regularization.ipynb) |
| [Autoencoders & GANs](AI_Engineer_Accelerator_Deep_Learning_Autoencoders_and_GANs.ipynb) | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/sunilmogadati/ai-engineer-accelerator/blob/main/AI_Engineer_Accelerator_Deep_Learning_Autoencoders_and_GANs.ipynb) |

### AI Applications

| Notebook | Open in Colab |
|:---|:---|
| [RAG from Scratch](AI_Engineer_Accelerator_RAG_from_Scratch.ipynb) — retrieval-augmented generation | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/sunilmogadati/ai-engineer-accelerator/blob/main/AI_Engineer_Accelerator_RAG_from_Scratch.ipynb) |
| [Agents](AI_Engineer_Accelerator_Agents.ipynb) — ReAct, tool use, multi-step reasoning | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/sunilmogadati/ai-engineer-accelerator/blob/main/AI_Engineer_Accelerator_Agents.ipynb) |
| [Multimodal AI](AI_Engineer_Accelerator_Multimodal_AI.ipynb) — vision, language, audio | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/sunilmogadati/ai-engineer-accelerator/blob/main/AI_Engineer_Accelerator_Multimodal_AI.ipynb) |

### Career

| Resource | Link |
|:---|:---|
| [Interview Prep](AI_Engineer_Interview_Prep.ipynb) — system design, portfolio, technical Q&A | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/sunilmogadati/ai-engineer-accelerator/blob/main/AI_Engineer_Interview_Prep.ipynb) |
| [Resume Template](AI_Engineer_Resume_Template.md) | [View](AI_Engineer_Resume_Template.md) |

---

## Pipeline Examples

End-to-end pipelines using a call center analytics dataset. The same data powers both the data engineering pipeline and the ML pipeline — mirroring how production systems work.

| Example | What It Demonstrates | Open in Colab |
|:---|:---|:---|
| [Analytics Pipeline](examples/simple_pipeline/Analytics_Pipeline.ipynb) | Bronze → Silver → Gold in Pandas | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/sunilmogadati/ai-engineer-accelerator/blob/main/examples/simple_pipeline/Analytics_Pipeline.ipynb) |
| [ML Pipeline](examples/simple_pipeline/ML_Pipeline.ipynb) | Feature engineering → train → evaluate → SHAP | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/sunilmogadati/ai-engineer-accelerator/blob/main/examples/simple_pipeline/ML_Pipeline.ipynb) |

---

## Projects

Structured specifications with requirements, deliverables, and evaluation criteria.

| Project | Focus |
|:---|:---|
| [P1: ML Predictor](projects/P1_ML_Predictor.md) | Binary classifier with cross-validation, SHAP, experiment tracking |
| [P1.5: Image Classifier](projects/P1_5_Deep_Learning_Image_Classifier.md) | PyTorch CNN on CIFAR-10 with training diagnostics |
| [P2: AI Eval & Cost](projects/P2_AI_Eval_Cost.md) | LLM evaluation harness — quality, latency, cost comparison |
| [P3: RAG Application](projects/P3_RAG_Application.md) | Document Q&A with RAGAS evaluation and prompt injection defense |

---

## The Dataset

All pipelines use a **call center analytics dataset** — synthetic data modeled on production DRTV (Direct Response Television) operations. Includes calls, campaigns, orders, products, and intentional data quality issues (duplicates, timezone bugs, missing values).

The companion [Data Engineering Reference](https://github.com/sunilmogadati/data-engineer-accelerator) builds the data pipeline that feeds these ML models — Bronze → Silver → Gold on GCP.

---

## Running Locally

```bash
git clone https://github.com/sunilmogadati/ai-engineer-accelerator.git
cd ai-engineer-accelerator
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
jupyter notebook
```

Or click any Colab badge above — zero local setup.

---

## Author

**Sunil Mogadati** — 25+ years building and leading complex systems end-to-end. Architect-Developer. Cloud, Data & AI. US Patent No. 10,638,891.

[LinkedIn](https://linkedin.com/in/sunilmogadati) · [Community](https://www.skool.com/workwise) · [GitHub](https://github.com/sunilmogadati)
