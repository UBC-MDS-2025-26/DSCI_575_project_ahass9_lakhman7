# Final Discussion

## Step 1: Improve Your Workflow

### Dataset Scaling

- **Number of products used**: 70,000 documents (reviews + metadata from All_Beauty category)
- This exceeds the minimum requirement of 10,000 products
- No changes to sampling strategy were needed — the 70k corpus was already built in Milestone 1 and reused throughout

### LLM Experiment

**Models compared:**

| Model | Family | Size |
|---|---|---|
| `llama-3.3-70b-versatile` | Llama 3.3 | 70B |
| `llama-3.1-8b-instant` | Llama 3.1 | 8B |

**Prompt used (same for both models):**

```
You are a helpful Amazon beauty product shopping assistant.
Answer the user's question using ONLY the provided product reviews and metadata.
Be concise, specific, and always reference the product title when making recommendations.
If the context does not contain enough information, say so honestly.
Context (retrieved product reviews):
[top-5 retrieved reviews]
User Question:
[query]
Answer based only on the above reviews:
```

**Results:**

**Query 1: "What is a good moisturizer for dry skin?"**

- llama-3.3-70b-versatile: Recommended 3 specific products with ASINs and ratings, clearly structured and concise.
- llama-3.1-8b-instant: Recommended similar products but included a typo in a review title ("great profuct") and was slightly less polished.

**Query 2: "Is there a good shampoo for hair loss?"**

- llama-3.3-70b-versatile: Honestly acknowledged limited evidence, clearly distinguished between a scalp scrubber and shampoos, and noted a low-rated hair loss shampoo.
- llama-3.1-8b-instant: Similar answer but added an unnecessary disclaimer about hair loss vs hair growth, making it slightly less focused.

**Query 3: "What are some highly rated anti-aging creams?"**

- llama-3.3-70b-versatile: Listed 3 products cleanly with ASINs and ratings.
- llama-3.1-8b-instant: Listed 2 products and added a note about a third product with mixed reviews — useful additional context but slightly verbose.

**Query 4: "Are there any good products for sensitive skin?"**

- llama-3.3-70b-versatile: Concise, well-structured, referenced 3 products with ratings.
- llama-3.1-8b-instant: Very similar output, slightly more list-based formatting.

**Query 5: "What is a good sunscreen for everyday use?"**

- llama-3.3-70b-versatile: Recommended 2 products concisely with clear justification.
- llama-3.1-8b-instant: Recommended an additional product not mentioned by the larger model, with good reasoning about why it suits everyday use.

**Key Observations:**

Overall, `llama-3.3-70b-versatile` produced more concise, polished, and consistently structured answers. It stayed closer to the retrieved context and avoided unnecessary elaboration. `llama-3.1-8b-instant` occasionally surfaced additional useful details (Query 5) but was less consistent in tone and formatting. For a product recommendation use case where clarity and conciseness matter, the 70B model is the better choice.

**Chosen model**: `llama-3.3-70b-versatile` remains the default as it produces higher quality, more reliable answers.

---

## Step 2: Additional Feature — Tool Integration (Option 2)

### What Was Implemented

A Tavily-powered web search tool was implemented in `src/tools.py`. It allows the RAG pipeline to be optionally augmented with live web results when the retrieved reviews do not contain sufficient information. In the Streamlit app, users can enable this via a checkbox in RAG Mode.

### Example Queries Where the Tool Was Used

**Query 1: "What is a good moisturizer for dry skin?"**

- RAG answer recommended products from the corpus
- Web search returned additional context from Vogue and Men's Health about ingredients like ceramides, hyaluronic acid, and glycerin
- The web results complemented the RAG answer with ingredient-level detail not present in reviews

**Query 2: "best natural deodorant without aluminum"**

- RAG answer cited specific products from reviews
- Web search returned current brand recommendations and dermatologist opinions
- Improved the answer by providing broader context beyond the 70k corpus

**Query 3: "What sunscreen doesn't leave a white cast?"**

- RAG answer found relevant reviews
- Web search surfaced Korean skincare recommendations and dermatologist-tested products
- The combination gave a more complete answer than either source alone

### Did It Improve Results?

Yes — the tool is most useful for queries where the review corpus lacks sufficient coverage or where current/external information adds value (e.g. ingredient science, trending products). For straightforward product queries well-covered by the corpus, the web search is redundant but not harmful.
## Step 3: Improve Documentation and Code Quality

### Documentation Update

The `README.md` was significantly expanded for the final submission. Key improvements include:

- Added a full project overview describing the end-to-end workflow: data ingestion, BM25 indexing, semantic indexing with ChromaDB, hybrid retrieval using Reciprocal Rank Fusion, RAG pipeline with Groq LLM, and optional Tavily web search augmentation
- Added separate sections describing each component: BM25 search, semantic search, hybrid retrieval, RAG pipeline, and tool integration
- Added clear setup instructions including environment setup, data download, index building, and app launch
- Added usage examples for both Search Only and RAG Mode tabs
- Added a description of new Milestone 3 features: LLM comparison, Tavily web search integration, and updated app interface

### Code Quality Changes

- All functions across `src/bm25.py`, `src/semantic.py`, `src/hybrid.py`, `src/utils.py`, `src/rag_pipeline.py`, `src/tools.py`, and `app/app.p- All functions across `src/bm25.py`, `src/seman all paths use `os.path.join(- All functions across `src/bm25.py`, `src/semantic.py`, `src/hybrid.py`, `src/utils.py`, `srrom `.env` (gitignored)
- `environment.yml` updated to include all dependencies including `tavily-python`, `groq`, `chromadb`, `sentence-transformers`, and `streamlit`
- `.gitignore` includes `.env`, `data/`, and `__pycache__`
- Temporary and junk files removed from repository

---

## Step 4: Cloud Deployment Plan

### Data Storage

**Raw data** (JSONL review and metadata files) would be stored in **AWS S3** in a versioned bucket (e.g. `s3://beauty-rag/data/raw/`). S3 is chosen for its low cost, durability, and native integration with other AWS services. Processed data (serialized corpus, pickled BM25 index) would also be stored in S3 (e.g. `s3://beauty-rag/data/processed/`), loaded into the app container at startup.

**Vector index** (ChromaDB) would be persisted to S3 and loaded into the app's local filesystem at container startup. For higher-traffic scenarios, it could be migrated to a managed vector database such as **Pinecone** or **Weaviate** to support concurrent reads without loading the full index into memory per instance.**Vector index** (ChromaDB) would be persisted to S3 and loaded into the app's local filesystem at container startup. For higher-traffic scenad,**Vector index** (ChromaDB) would be persisted to S3 and e.**Vector index** (ChromaDB) would be persisted tomli**app**Vector index** (ChromaDB) woucker and deployed on **Vector index** (ChromaDB) would be persisted to S3 and loaded into the app's local filesystem at container startup. For higher-traffic scenarios, it could be migrated to a managed vector database such as **Pinecone** or **Weaviate** to support concurrent reads without loading the full index into memory per instance.**Vector index** (ChromaDB) would be persisted to S3 and loaded into th can each load their own copy without conflict. For higher scale, indices could be moved to a shared managed service (Pinecone, OpenSearch) to avoid redundant loading.

**LLM inference**: The pipeline uses the **Groq API** (`llama-3.3-70b-versatile`) for LLM inference. This is a managed API approach — no GPU instances are required. Groq handles model hosting and provides low-latency inference. This is the right choice for this use case: it avoids the operational complexity and cost of self-hosting a 70B model on a GPU instance. If data privacy requirements precluded external APIs, the alternative would be deploying a smaller quantized model on an AWS EC2 `g4dn` GPU instance.

### Streaming / Updates

**Incorporating new products**: New reviews would be ingested via a scheduled **AWS Lambda** function or **AWS Glue** ETL job triggered on a weekly or monthly cadence. The job would download new review data, preprocess it using `src/utils.py`, and append new documents to the corpus.

**Index updates**: New documen**Index updates**: New documen**Index updates**: New documen**Index updates**: New documen**Index updates**: New documen**Index updates**: New documen**Index updatemental updates). Both updated indices would be re-uploaded to S3 and ECS tasks restarted to pick up the new versions.

**Architectural justification**: The batch re-indexing approach is appropriate here because beauty product reviews do not change in real time — weekly or monthly updates are sufficient. A streaming pipeline (e.g. Kafka + real-time index updates) would add significant complexity without meaningful benefit for this use case.
