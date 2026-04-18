import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from dotenv import load_dotenv
from src.utils import load_pickle
from src.bm25 import bm25_search
from src.semantic import semantic_search
from src.rag_pipeline import load_vector_store, rag_pipeline
from src.hybrid import hybrid_rag_pipeline
from src.tools import web_search

load_dotenv()

st.set_page_config(
    page_title="Beauty Product Search",
    page_icon="💄",
    layout="wide"
)

st.title("💄 Beauty Product Search")
st.markdown("Search Amazon All_Beauty reviews using BM25, Semantic Search, or RAG.")