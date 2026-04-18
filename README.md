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