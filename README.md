# DSCI 575 Project — Beauty Product Retrieval System

A retrieval system for Amazon All_Beauty product reviews using BM25 keyword search and semantic search with sentence embeddings.

---

## Team Members
- Ashifa Hassam (ahass9)
- Gurleen Kaur (lakhman7)

## Project Overview

This project builds an information retrieval system over the [Amazon Reviews 2023](https://amazon-reviews-2023.github.io/) dataset (All_Beauty category). It implements and compares two retrieval approaches:

- **BM25**: keyword-based retrieval using the `rank-bm25` library
- **Semantic Search**: embedding-based retrieval using `sentence-transformers` and `ChromaDB`

A simple Streamlit web app allows users to interactively query the retrieval system.

## Dataset

- **Source**: [Amazon Reviews 2023](https://amazon-reviews-2023.github.io/)
- **Category**: All_Beauty
- **Files**:
  - `All_Beauty.jsonl.gz` — user reviews, ratings, timestamps
  - `meta_All_Beauty.jsonl.gz` — product titles, descriptions, features

Download the files and place them in `data/raw/`. They are excluded from version control via `.gitignore`.

```bash
curl -o data/raw/All_Beauty.jsonl.gz "https://datarepo.eng.ucsd.edu/mcauley_group/data/amazon_2023/raw/review_categories/All_Beauty.jsonl.gz"

curl -o data/raw/meta_All_Beauty.jsonl.gz "https://datarepo.eng.ucsd.edu/mcauley_group/data/amazon_2023/raw/meta_categories/meta_All_Beauty.jsonl.gz"
```

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/UBC-MDS/DSCI_575_project_ahass9_lakhman7.git
cd DSCI_575_project_ahass9_lakhman7
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # Mac/Linux
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Create a `.env` file in the project root (never commit this):

```
# Add any API keys here if needed in later milestones
```

## Repository Structure

```
DSCI_575_project_ahass9_lakhman7/
│
├── README.md
├── requirements.txt
├── .env                        # never commit secrets
│
├── data/
│   ├── raw/                    # downloaded .jsonl.gz files (gitignored)
│   └── processed/              # cleaned and indexed files
│
├── notebooks/
│   └── milestone1_exploration.ipynb
│
├── src/
│   ├── bm25.py                 # BM25 retrieval
│   ├── semantic.py             # Semantic retrieval
│   └── utils.py                # Preprocessing and corpus utilities
│
├── results/
│   └── milestone1_discussion.md
│
└── app/
    └── app.py                  # Streamlit web app
```

## Workflow

### 1. Data Exploration
Open and run `notebooks/milestone1_exploration.ipynb` to explore and preprocess the dataset.

### 2. BM25 Retrieval
`src/bm25.py` builds and queries a BM25 index over the processed corpus.

### 3. Semantic Retrieval
`src/semantic.py` generates embeddings using `all-MiniLM-L6-v2` and stores them in a ChromaDB vector store for similarity search.

### 4. Running the App

```bash
streamlit run app/app.py
```

## Retrieval Methods

| Method | Library | Index |
|---|---|---|
| BM25 | `rank-bm25` | Pickled BM25 object |
| Semantic | `sentence-transformers` + `ChromaDB` | Persistent Chroma vector store |

---

## Results and Discussion

See `results/milestone1_discussion.md` for qualitative evaluation across 10 queries comparing BM25 and semantic search.