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

