import os
from groq import Groq
from dotenv import load_dotenv
import chromadb
from sentence_transformers import SentenceTransformer

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def load_vector_store(persist_dir="data/processed/chroma", collection_name="beauty_reviews"):
    """Load the existing ChromaDB collection from Milestone 1."""
    chroma_client = chromadb.PersistentClient(path=persist_dir)
    collection = chroma_client.get_collection(collection_name)
    model = SentenceTransformer('all-MiniLM-L6-v2')
    print(f"Loaded collection with {collection.count()} documents")
    return collection, model

def semantic_retriever(query, collection, model, top_k=5):
    """Retrieve top-k relevant documents using semantic search."""
    query_embedding = model.encode(query).tolist()
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )
    
    docs = []
    for i in range(len(results['ids'][0])):
        docs.append({
            'id': results['ids'][0][i],
            'text': results['documents'][0][i],
            'metadata': results['metadatas'][0][i],
            'distance': results['distances'][0][i]
        })
    
    return docs

def build_context(docs):
    """Convert retrieved documents into a prompt-ready context block."""
    context_parts = []
    for i, doc in enumerate(docs, 1):
        context_parts.append(
            f"[{i}] Product: {doc['metadata'].get('display_title', 'N/A')}\n"
            f"    ASIN: {doc['metadata'].get('asin', 'N/A')}\n"
            f"    Rating: {doc['metadata'].get('rating', 'N/A')}/5\n"
            f"    Review: {doc['metadata'].get('review_text', 'N/A')}"
        )
    return "\n\n".join(context_parts)

