# Milestone 2 Discussion: RAG Pipeline Evaluation

## 1. Model Choice

### LLM: Llama-3.3-70B-Versatile via Groq API
We chose `llama-3.3-70b-versatile` served through the Groq API for the following reasons:

**Model choice rationale:**
- Llama 3.3 70B is Meta's strongest openly available instruction-tuned model, scoring 86.0% on MMLU
- It supports tool use, JSON mode, and 128K context length — useful for RAG workflows with large contexts
- The Groq API provides extremely fast inference without requiring local GPU resources

**Model size rationale:**
- The 70B parameter model was chosen over smaller alternatives (e.g. 8B) because RAG requires the model to synthesize multiple retrieved documents and produce accurate, grounded answers
- Smaller models (e.g. 8B) tend to hallucinate more when asked to stay strictly within a provided context
- The free Groq API tier supports 70B inference at no cost, making it practical for this project

---

## 2. Qualitative Evaluation of Hybrid RAG

Each query is rated on three dimensions (Yes/No):
- **Accuracy**: Is the answer factually correct based on the reviews?
- **Completeness**: Does the answer address all aspects of the question?
- **Fluency**: Is the answer natural, clear, and easy to read?

---

### Query 1: "What is a good moisturizer for dry skin?"

**Answer:**
For dry skin, I would recommend the "daytime moisturizer for dry skin" (B01M1A0H4Z) with a 4.0/5 rating, or the "really great moisturizer for eczema or chronically dry skin" (B07N9M4N54) with a 5.0/5 rating, as both products have positive reviews from users with dry skin.

| Dimension | Rating | Notes |
|---|---|---|
| Accuracy | Yes | Products cited match the retrieved reviews |
| Completeness | Yes | Covers multiple options with ratings |
| Fluency | Yes | Clear and well-structured response |

---

### Query 2: "Is there a good shampoo for hair loss?"

**Answer:**
Based on the provided reviews, the "scalp scrubber" (ASIN: B08C9T688H) with a 5.0/5 rating seems to have helped the reviewer with hair loss, but it's not a shampoo. For shampoos, the "antihair loss shampoo hair regrowth shampoo" (ASIN: B076D59KHX) has a 1.0/5 rating and did not work for the reviewer. More information would be needed to determine if it's effective for hair loss.

| Dimension | Rating | Notes |
|---|---|---|
| Accuracy | Yes | Correctly reflects what the reviews say |
| Completeness | Partial | Acknowledges lack of strong evidence honestly |
| Fluency | Yes | Clear and well-written |

---

### Query 3: "What are some highly rated anti-aging creams?"

**Answer:**
Based on the reviews, I recommend the "anti aging cream" (ASIN: B07T3ZFXYF) with a 5.0/5 rating, the "anti aging wrinkle cream" (ASIN: B00K58HQRM) with a 5.0/5 rating, and the "best anti aging face cream with both retinol and hyaluronic acid" (ASIN: B00NK65R5O) also with a 5.0/5 rating.

| Dimension | Rating | Notes |
|---|---|---|
| Accuracy | Yes | All cited products match retrieved reviews |
| Completeness | Yes | Provides multiple options with ratings |
| Fluency | Yes | Concise and easy to read |

---

### Query 4: "Are there any good products for sensitive skin?"

**Answer:**
Yes, there are several good products for sensitive skin. Consider the "gentle" product (B01IAI4SAQ) with a 5.0/5 rating. Another option is the "gret product" (B000H3I0PW), also rated 5.0/5. Additionally, the "just what you need for sensitive skin" product (B08GCTZGZD) with a 5.0/5 rating cleans well and doesn't aggravate extremely sensitive skin.

| Dimension | Rating | Notes |
|---|---|---|
| Accuracy | Yes | Grounded in retrieved reviews |
| Completeness | Yes | Multiple products with ratings provided |
| Fluency | Yes | Natural and readable |

---

### Query 5: "What is a good sunscreen for everyday use?"

**Answer:**
For everyday use, I recommend the "best sunscreen" (ASIN: B07T4SJJFX) with a 5.0/5 rating. Alternatively, consider the "pure sun defense sunscreen lotion frozen 50 8 oz" (ASIN: B00WVYH4HA) with a 5.0/5 rating, which worked well for the reviewer on the beach.

| Dimension | Rating | Notes |
|---|---|---|
| Accuracy | Yes | Reflects retrieved review content accurately |
| Completeness | Partial | Could include more options |
| Fluency | Yes | Clear and concise |

---

## 3. Key Observations

Overall, the Hybrid RAG system performs well on straightforward product recommendation queries, consistently grounding answers in retrieved reviews and citing ASINs and ratings. The system handles both specific queries (e.g. sunscreen) and broader ones (e.g. sensitive skin) effectively. However, for niche queries like hair loss shampoos, the retriever struggles to find strongly relevant documents, and the LLM honestly acknowledges this limitation rather than hallucinating — a positive behaviour. The fluency of generated answers is consistently high across all queries, reflecting the strength of the Llama 3.3 70B model.

---

## 4. Limitations of the Hybrid RAG Workflow

1. **Keyword-semantic imbalance**: In our evaluation, the hybrid retriever returned predominantly semantic search results, with BM25 contributing little to the final ranked list. This suggests the RRF weighting (40% BM25, 60% semantic) may need tuning, or that the BM25 index needs to be persisted and reused rather than rebuilt each time.

2. **No factual verification**: The LLM is instructed to answer only from the provided context, but it cannot verify whether the reviews themselves are accurate or trustworthy. A highly-rated product with few reviews may be over-represented in the retrieved context, leading to potentially misleading recommendations.

---

## 5. Suggestions for Future Improvements

1. **Persist the BM25 index**: Currently the BM25 index is rebuilt from scratch every run, which takes significant time. Saving and loading it from disk (as a pickle file) would make the hybrid retriever much faster in production.

2. **Re-rank with a cross-encoder**: After the hybrid retrieval step, applying a cross-encoder re-ranker (e.g. `cross-encoder/ms-marco-MiniLM-L-6-v2`) would significantly improve result relevance by scoring query-document pairs jointly rather than independently.

3. **Tune RRF weights**: Systematically evaluate different BM25/semantic weight combinations to find the optimal balance for beauty product queries.