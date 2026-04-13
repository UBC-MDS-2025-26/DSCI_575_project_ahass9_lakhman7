import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rank_bm25 import BM25Okapi
from src.utils import preprocess_text, load_corpus, save_pickle, load_pickle


def tokenize(text):
    """Tokenize text by whitespace after preprocessing."""
    return preprocess_text(text).split()

