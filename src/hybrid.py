import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from groq import Groq
from dotenv import load_dotenv
from src.bm25 import bm25_search, tokenize
from src.rag_pipeline import semantic_retriever, build_context, build_prompt

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def bm25_retriever(query, bm25, corpus, top_k=5):
    """
    BM25 retriever that returns top-k documents in a standard format.
    
    Parameters
    ----------
    query : str
        The search query.
    bm25 : BM25Okapi
        The BM25 index.
    corpus : list of dict
        The original corpus.
    top_k : int
        Number of results to return.
    
    Returns
    -------
    list of dict
        Top k results with id, text, metadata, and score.
    """
    results = bm25_search(query, bm25, corpus, top_k=top_k)
    
    docs = []
    for r in results:
        docs.append({
            'id': str(r['doc_id']),
            'text': r['text'],
            'metadata': {
                'asin': r['asin'],
                'display_title': r['display_title'],
                'review_text': r['review_text'],
                'rating': float(r['rating']) if r['rating'] else 0.0
            },
            'score': r['score'],
            'source': 'bm25'
        })
    
    return docs

def hybrid_retriever(query, bm25, corpus, collection, model, top_k=5, bm25_weight=0.4, semantic_weight=0.6):
    """
    Hybrid retriever combining BM25 and semantic search using Reciprocal Rank Fusion.
    
    Parameters
    ----------
    query : str
        The search query.
    bm25 : BM25Okapi
        The BM25 index.
    corpus : list of dict
        The original corpus.
    collection : chromadb collection
        The ChromaDB collection.
    model : SentenceTransformer
        The sentence transformer model.
    top_k : int
        Number of results to return.
    bm25_weight : float
        Weight for BM25 results.
    semantic_weight : float
        Weight for semantic results.
    
    Returns
    -------
    list of dict
        Top k re-ranked results.
    """
    # Get results from both retrievers
    bm25_results = bm25_retriever(query, bm25, corpus, top_k=top_k)
    semantic_results = semantic_retriever(query, collection, model, top_k=top_k)

    # Reciprocal Rank Fusion
    k = 60  # RRF constant
    scores = {}
    docs_map = {}

    for rank, doc in enumerate(bm25_results):
        doc_id = doc['id']
        scores[doc_id] = scores.get(doc_id, 0) + bm25_weight * (1 / (k + rank + 1))
        doc['source'] = 'bm25'
        docs_map[doc_id] = doc

    for rank, doc in enumerate(semantic_results):
        doc_id = doc['id']
        scores[doc_id] = scores.get(doc_id, 0) + semantic_weight * (1 / (k + rank + 1))
        if doc_id not in docs_map:
            doc['source'] = 'semantic'
            docs_map[doc_id] = doc

    # Sort by RRF score and return top_k
    ranked_ids = sorted(scores, key=lambda x: scores[x], reverse=True)[:top_k]
    return [docs_map[doc_id] for doc_id in ranked_ids]

def hybrid_rag_pipeline(query, bm25, corpus, collection, model, top_k=5):
    """
    Full RAG pipeline using hybrid retriever.
    
    Parameters
    ----------
    query : str
        The search query.
    bm25 : BM25Okapi
        The BM25 index.
    corpus : list of dict
        The original corpus.
    collection : chromadb collection
        The ChromaDB collection.
    model : SentenceTransformer
        The sentence transformer model.
    top_k : int
        Number of results to return.
    
    Returns
    -------
    dict
        Query, answer, and retrieved docs.
    """
    # Step 1: Hybrid retrieval
    docs = hybrid_retriever(query, bm25, corpus, collection, model, top_k=top_k)
    
    # Step 2: Building context
    context = build_context(docs)
    
    # Step 3: Building prompt
    prompt = build_prompt(query, context)
    
    # Step 4: Calling LLM
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=512
    )
    
    answer = response.choices[0].message.content
    
    return {
        "query": query,
        "answer": answer,
        "retrieved_docs": docs
    }

if __name__ == "__main__":
    from src.utils import load_corpus
    from src.bm25 import build_bm25_index
    from src.rag_pipeline import load_vector_store

    reviews_path = os.path.join('data', 'raw', 'All_Beauty.jsonl')
    meta_path = os.path.join('data', 'raw', 'meta_All_Beauty.jsonl')

    print("Loading corpus...")
    corpus = load_corpus(reviews_path, meta_path, max_rows=70000)

    print("Building BM25 index...")
    bm25, _ = build_bm25_index(corpus)

    print("Loading vector store...")
    collection, model = load_vector_store()

    query = "What is a good moisturizer for dry skin?"
    print(f"\nRunning hybrid RAG for: '{query}'")
    result = hybrid_rag_pipeline(query, bm25, corpus, collection, model)

    print(f"\nAnswer:\n{result['answer']}")
    print(f"\nRetrieved {len(result['retrieved_docs'])} documents")
    for i, doc in enumerate(result['retrieved_docs'], 1):
        print(f"{i}. [{doc.get('source', 'N/A')}] {doc['metadata']['display_title']} (rating: {doc['metadata']['rating']})")

    