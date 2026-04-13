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