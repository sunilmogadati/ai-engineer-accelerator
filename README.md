# AI Engineer Accelerator — Interactive Notebooks

**By Sunil Mogadati** | AI Engineer Accelerator

Interactive guides, interview prep, and career resources for aspiring AI Engineers. Every cell is runnable. No slides, no fluff — just code and concepts.

---

## The Notebooks

### 1. Python for AI Engineers
> Comprehensive Python foundation — data types through OOP, logging, testing, and project structure.

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/sunilmogadati/ai-engineer-accelerator/blob/main/AI_Engineer_Accelerator_Python_for_AI.ipynb)

### 2. Python for AI — Java Developer's Express Guide
> Already know Java? Skip the basics. This maps Java concepts to Python in ~2 hours. Covers NumPy, Pandas, Matplotlib, and Scikit-learn.

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/sunilmogadati/ai-engineer-accelerator/blob/main/Python_for_AI_Java_Dev_Guide.ipynb)

### 3. Database Essentials for AI Engineers
> SQL, NoSQL, and Vector Databases — from SQLite basics through ChromaDB semantic search to production patterns. Includes installation guides, real-world scenarios, and hands-on exercises.

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/sunilmogadati/ai-engineer-accelerator/blob/main/AI_Engineer_Accelerator_Database_Essentials.ipynb)

### 4. Math for AI Engineers
> Vectors, cosine similarity, matrices, probability, gradient descent, loss functions, backpropagation, PCA — the math that makes ML make sense.

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/sunilmogadati/ai-engineer-accelerator/blob/main/AI_Engineer_Accelerator_Math_for_AI.ipynb)

### 5. Interview Prep
> Coding exercises, ML theory Q&A, system design walkthroughs, behavioral prep, and study plans. 39 cells, no API keys needed.

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/sunilmogadati/ai-engineer-accelerator/blob/main/AI_Engineer_Interview_Prep.ipynb)

### 6. Resume Template
> Composite AI Engineer job posting, annotated resume template, ATS optimization tips, and Accelerator-to-resume skill mapping.

[View Resume Template](AI_Engineer_Resume_Template.md)

---

## How to Run

### Option 1: Google Colab (zero setup)
Click any "Open in Colab" badge above. All you need is a Google account.

### Option 2: GitHub Codespaces (full VS Code in browser)
Click **Code** → **Codespaces** → **Create codespace on main**. A full development environment launches in your browser with all dependencies pre-installed.

### Option 3: Run Locally
```bash
git clone https://github.com/sunilmogadati/ai-engineer-accelerator.git
cd ai-engineer-accelerator
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
jupyter notebook
```

---

## What's Inside

| Notebook | Sections | Code Cells | Audience |
|----------|----------|------------|----------|
| Python for AI Engineers | 21 sections | 25+ | Beginners / career switchers |
| Java Dev Express Guide | 5 parts | 20+ | Experienced Java/Scala developers |
| Database Essentials | 22 sections | 22+ | All AI engineers |
| Math for AI Engineers | 14 sections | 12+ | All AI engineers |
| Interview Prep | 9 sections | 18 | Job seekers |
| Resume Template | 6 sections | — | Job seekers |

### Topics Covered

**Python Notebook:** Data types, strings, collections, control flow, functions, OOP (4 pillars), error handling, logging, file I/O, imports, virtual environments, pip, testing with pytest, Git basics, SQL overview.

**Java Dev Guide:** Python syntax mapped from Java, list comprehensions, NumPy (vectorized ops, broadcasting), Pandas (DataFrames, groupby, merge), Matplotlib, Scikit-learn (fit/predict pattern).

**Database Notebook:** SQLite (CRUD, JOINs, transactions, parameterized queries), PostgreSQL, ChromaDB (semantic search, metadata filtering), Redis (caching patterns), MongoDB (document model), SQLAlchemy ORM, vector DB trade-offs (ChromaDB vs Pinecone vs Weaviate vs pgvector), AI/ML-specific databases (feature stores, experiment trackers), MCP database tools, connection security.

---

## Dependencies

**Zero-install (works immediately):**
- All SQLite cells — `sqlite3` is built into Python

**One install:**
- ChromaDB cells — `pip install chromadb`

**Optional:**
- SQLAlchemy — `pip install sqlalchemy`
- python-dotenv — `pip install python-dotenv`

See `requirements.txt` for the full list.

---

## License

These materials are part of the AI Engineer Accelerator program.

---

**Questions?** Connect with [Sunil Mogadati on LinkedIn](https://linkedin.com/in/sunilmogadati).
