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

