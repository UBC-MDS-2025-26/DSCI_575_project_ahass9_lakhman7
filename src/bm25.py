import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rank_bm25 import BM25Okapi
from src.utils import preprocess_text, load_corpus, save_pickle, load_pickle


def tokenize(text):
    """Tokenize text by whitespace after preprocessing."""
    return preprocess_text(text).split()

def build_bm25_index(corpus):
    """
    Build a BM25 index from the corpus.
    
    Parameters
    ----------
    corpus : list of dict
        Each dict contains a 'text' field.
    
    Returns
    -------
    tuple
        (bm25 object, tokenized corpus)
    """
    print("Tokenizing corpus...")
    tokenized_corpus = [tokenize(doc['text']) for doc in corpus]
    
    print("Building BM25 index...")
    bm25 = BM25Okapi(tokenized_corpus)
    
    print("BM25 index built successfully")
    return bm25, tokenized_corpus

def bm25_search(query, bm25, corpus, top_k=5):
    """
    Search the BM25 index for the given query.
    
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
        Top k results with scores.
    """
    tokenized_query = tokenize(query)
    scores = bm25.get_scores(tokenized_query)
    
    top_indices = scores.argsort()[::-1][:top_k]
    
    results = []
    for idx in top_indices:
        result = corpus[idx].copy()
        result['score'] = round(float(scores[idx]), 4)
        results.append(result)
    
    return results

if __name__ == "__main__":
    import os

    reviews_path = os.path.join('data', 'raw', 'All_Beauty.jsonl')
    meta_path = os.path.join('data', 'raw', 'meta_All_Beauty.jsonl')

    # Load corpus
    corpus = load_corpus(reviews_path, meta_path)

    # Build index
    bm25, tokenized_corpus = build_bm25_index(corpus)

    # Save
    save_pickle(bm25, os.path.join('data', 'processed', 'bm25_index.pkl'))
    save_pickle(corpus, os.path.join('data', 'processed', 'corpus.pkl'))
    save_pickle(tokenized_corpus, os.path.join('data', 'processed', 'tokenized_corpus.pkl'))

    # Test search
    query = "moisturizer for dry skin"
    results = bm25_search(query, bm25, corpus, top_k=5)
    print(f"\nTop 5 results for: '{query}'")
    for i, r in enumerate(results):
        print(f"\n{i+1}. {r['display_title']}")
        print(f"   Score: {r['score']}")
        print(f"   Rating: {r['rating']}")


        