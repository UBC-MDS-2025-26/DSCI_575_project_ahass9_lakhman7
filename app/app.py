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

@st.cache_resource
def load_bm25():
    bm25 = load_pickle(os.path.join('data', 'processed', 'bm25_index.pkl'))
    corpus = load_pickle(os.path.join('data', 'processed', 'corpus.pkl'))
    return bm25, corpus

@st.cache_resource
def load_semantic():
    collection, model = load_vector_store()
    return collection, model

tab1, tab2 = st.tabs(["🔍 Search Only", "🤖 RAG Mode"])

with tab1:
    st.markdown("### Search Amazon Beauty Reviews")
    method = st.radio("Retrieval Method", ["BM25", "Semantic"], horizontal=True)
    top_k = st.slider("Number of results", min_value=1, max_value=10, value=5)
    query = st.text_input("Enter your search query", placeholder="e.g. moisturizer for dry skin", key="search_query")

    if query:
        if method == "BM25":
            with st.spinner("Searching with BM25..."):
                bm25, corpus = load_bm25()
                results = bm25_search(query, bm25, corpus, top_k=top_k)
        else:
            with st.spinner("Searching with Semantic Search..."):
                collection, model = load_semantic()
                results = semantic_search(query, collection, model, top_k=top_k)

        st.markdown(f"### Results for: *{query}*")
        for i, r in enumerate(results):
            st.markdown("---")
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"**{i+1}. {r['display_title'].title()}**")
                st.markdown(f"📝 {r['review_text'][:200]}...")
            with col2:
                rating = r.get('rating', 0)
                stars = "⭐" * int(rating)
                st.markdown(f"{stars} ({rating})")
                st.markdown(f"**Score:** `{r['score']}`")