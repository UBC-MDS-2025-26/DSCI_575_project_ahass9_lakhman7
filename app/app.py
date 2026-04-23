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
    """Load the BM25 index and corpus from disk."""
    bm25 = load_pickle(os.path.join('data', 'processed', 'bm25_index.pkl'))
    corpus = load_pickle(os.path.join('data', 'processed', 'corpus.pkl'))
    return bm25, corpus

@st.cache_resource
def load_semantic():
    """Load the ChromaDB collection and sentence transformer model."""
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

with tab2:
    st.markdown("### RAG Mode — Ask a Question")
    rag_query = st.text_input("Enter your question", placeholder="e.g. What is a good moisturizer for dry skin?", key="rag_query")
    use_web_search = st.checkbox("🌐 Augment with web search (Tavily)", value=False)
    top_k_rag = st.slider("Number of documents to retrieve", min_value=1, max_value=10, value=5, key="rag_slider")

    if rag_query:
        with st.spinner("Running Hybrid RAG pipeline..."):
            bm25, corpus = load_bm25()
            collection, model = load_semantic()
            result = hybrid_rag_pipeline(rag_query, bm25, corpus, collection, model, top_k=top_k_rag)

        st.success("💡 **RAG Answer:**")
        st.markdown(f"> {result['answer']}")

        if use_web_search:
            st.markdown("---")
            st.markdown("### 🌐 Web Search Results")
            with st.spinner("Searching the web..."):
                web_results = web_search(rag_query)
            st.markdown(web_results)

        st.markdown("---")
        st.markdown("### 📚 Retrieved Documents")
        for i, doc in enumerate(result['retrieved_docs']):
            st.markdown("---")
            col1, col2 = st.columns([3, 1])
            with col1:
                title = doc['metadata'].get('display_title', 'N/A').title()
                review = doc['metadata'].get('review_text', 'N/A')
                st.markdown(f"**{i+1}. {title}**")
                st.markdown(f"📝 {review[:200]}...")
            with col2:
                rating = doc['metadata'].get('rating', 0)
                stars = "⭐" * int(rating)
                st.markdown(f"{stars} ({rating})")
                source = doc.get('source', 'N/A')
                st.markdown(f"**Source:** `{source}`")