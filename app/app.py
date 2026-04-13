import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from sentence_transformers import SentenceTransformer
import chromadb

from src.utils import load_corpus, load_pickle
from src.bm25 import bm25_search
from src.semantic import semantic_search

st.set_page_config(
    page_title="Beauty Product Search",
    page_icon="💄",
    layout="wide"
)

st.title("💄 Beauty Product Search")
st.markdown("Search through Amazon All_Beauty reviews using BM25 or Semantic Search.")