# DSCI 575 Project — Beauty Product Retrieval System

A retrieval system for Amazon All_Beauty product reviews using BM25 keyword search, semantic search, and a RAG pipeline powered by Groq LLM.

---

## Team Members
- Ashifa Hassam (ahass9)
- Gurleen Kaur (lakhman7)

---

## Project Overview

This project builds an information retrieval and question-answering system over the [Amazon Reviews 2023](https://amazon-reviews-2023.github.io/) dataset (All_Beauty category). It implements and compares retrieval approaches and integrates a full RAG pipeline:

- **BM25**: keyword-based retrieval using the `rank-bm25` library
- **Semantic Search**: embedding-based retrieval using `sentence-transformers` and `ChromaDB`
- **Hybrid Retrieval**: combines BM25 and semantic search using Reciprocal Rank Fusion
- **RAG Pipeline**: retrieves relevant reviews and generates grounded answers using Groq's `llama-3.3-70b-versatile`
- **Web Search Tool**: augments RAG answers with live web results using the Tavily API

A Streamlit web app allows users to interactively search reviews or ask questions using the RAG pipeline.

---

## Dataset

- **Source**: [Amazon Reviews 2023](https://amazon-reviews-2023.github.io/)
- **Category**: All_Beauty
- **Files**:
  - `All_Beauty.jsonl` — user reviews, ratings, timestamps
  - `meta_All_Beauty.jsonl` — product titles, descriptions, features

Download the files and place them in `data/raw/`. They are excluded from version control via `.gitignore`.

```bash
curl -L -o data/raw/All_Beauty.jsonl "https://huggingface.co/datasets/McAuley-Lab/Amazon-Reviews-2023/resolve/main/raw/review_categories/All_Beauty.jsonl"

curl -L -o data/raw/meta_All_Beauty.jsonl "https://huggingface.co/datasets/McAuley-Lab/Amazon-Reviews-2023/resolve/main/raw/meta_categories/meta_All_Beauty.jsonl"
```

---

## Data Processing

Raw data is loaded and preprocessed in `src/utils.py`. The pipeline joins review data with product metadata on the `asin` field.

**Fields used from reviews (`All_Beauty.jsonl`):**
- `asin` — product identifier for joining with metadata
- `rating` — numeric star rating (1–5)
- `text` — review body text

**Fields used from metadata (`meta_All_Beauty.jsonl`):**
- `asin` — product identifier
- `title` — product display title
- `description` — product description
- `features` — product features joined into a single string

**Preprocessing steps** (applied in `preprocess_text()`):
1. Lowercase all text
2. Remove punctuation
3. Strip extra whitespace

The full corpus is serialized to `data/processed/corpus.pkl` for reuse across BM25 and semantic indexing.

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/UBC-MDS/DSCI_575_project_ahass9_lakhman7.git
cd DSCI_575_project_ahass9_lakhman7
```

### 2. Create and activate the conda environment

```bash
conda env create -f environment.yml
conda activate 575-beauty-retrieval
```

### 3. Set up environment variables

Create a `.env` file in the project root (never commit this) and add your API keys:

```
GROQ_API_KEY=your_groq_key_here
TAVILY_API_KEY=your_tavily_key_here
```

- Get a free Groq API key at https://console.groq.com
- Get a free Tavily API key at https://app.tavily.com

---

## Repository Structure

```
DSCI_575_project_ahass9_lakhman7/
│
├── README.md
├── requirements.txt
├── environment.yml
├── .env                          # never commit secrets
│
├── data/
│   ├── raw/                      # downloaded .jsonl files (gitignored)
│   └── processed/                # indexes and embeddings (gitignored)
│
├── notebooks/
│   ├── milestone1_exploration.ipynb
│   └── milestone2_rag.ipynb
│
├── src/
│   ├── utils.py                  # preprocessing and corpus utilities
│   ├── bm25.py                   # BM25 retrieval
│   ├── semantic.py               # semantic retrieval
│   ├── rag_pipeline.py           # RAG pipeline with semantic retrieval
│   ├── hybrid.py                 # hybrid retriever and hybrid RAG pipeline
│   └── tools.py                  # Tavily web search tool
│
├── results/
│   ├── milestone1_discussion.md
│   └── milestone2_discussion.md
│
└── app/
    └── app.py                     # Streamlit web app
```

---

## Workflow

### 1. Data Exploration
Open and run `notebooks/milestone1_exploration.ipynb` to explore and preprocess the dataset.

### 2. Build BM25 Index
```bash
python src/bm25.py
```

### 3. Build Semantic Index
```bash
python src/semantic.py
```

### 4. Run RAG Pipeline
```bash
python src/rag_pipeline.py
```

### 5. Run Hybrid RAG Pipeline
```bash
python src/hybrid.py
```

### 6. Launch the App
```bash
streamlit run app/app.py
```

---

## Retrieval Methods

| Method | Library | Index |
|---|---|---|
| BM25 | `rank-bm25` | Pickled BM25 object |
| Semantic | `sentence-transformers` + `ChromaDB` | Persistent Chroma vector store |
| Hybrid | BM25 + Semantic with Reciprocal Rank Fusion | Combined |

---

### BM25 (`src/bm25.py`)
BM25 is a classical keyword-based ranking function. Each document is tokenized by preprocessing (lowercase, remove punctuation, split on whitespace) and indexed using the `rank-bm25` library. At query time, the query is tokenized the same way and scored against all documents using the BM25 formula, which accounts for term frequency, inverse document frequency, and document length normalization. The top-k highest scoring documents are returned. The index is saved to `data/processed/bm25_index.pkl` for reuse.

**Returns per result:** `display_title`, `review_text`, `rating`, `asin`, BM25 `score`

### Semantic Search (`src/semantic.py`)
Semantic search uses dense vector embeddings to find documents semantically similar to a query, even if they share no keywords. Each document is embedded using `all-MiniLM-L6-v2` from `sentence-transformers` and stored in a persistent ChromaDB vector store at `data/processed/chroma/`. At query time, the query is embedded using the same model and the top-k nearest neighbours are retrieved by cosine similarity. Embeddings are computed once and persisted to avoid recomputation.

**Returns per result:** `display_title`, `review_text`, `rating`, `asin`, similarity `score`

---

## RAG Pipeline

The RAG pipeline (`src/rag_pipeline.py`) follows three stages:

1. **Retriever**: semantic search retrieves top-k relevant reviews from ChromaDB
2. **Context Builder**: formats retrieved reviews into a structured prompt
3. **LLM Generator**: Groq's `llama-3.3-70b-versatile` generates a grounded answer

The hybrid RAG pipeline (`src/hybrid.py`) replaces the semantic retriever with a hybrid retriever that combines BM25 and semantic search using Reciprocal Rank Fusion (RRF), weighting BM25 at 40% and semantic search at 60%.

---

## Web Search Tool

`src/tools.py` implements a Tavily-powered web search tool that can augment RAG answers with live web results. In the app, users can optionally enable this tool in RAG Mode to supplement review-based answers with current information from the web.

---

## Results and Discussion

- `results/milestone1_discussion.md` — qualitative evaluation of BM25 vs semantic search across 10 queries
- `results/milestone2_discussion.md` — qualitative evaluation of the hybrid RAG pipeline across 5 queries, including model choice rationale, key observations, limitations, and future improvements