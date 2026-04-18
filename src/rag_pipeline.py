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

