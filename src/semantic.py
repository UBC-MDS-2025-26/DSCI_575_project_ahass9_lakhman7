import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sentence_transformers import SentenceTransformer
import chromadb
from src.utils import load_corpus, load_pickle

def build_semantic_index(corpus, collection_name="beauty_reviews", persist_dir="data/processed/chroma"):
    """
    Build a semantic index using sentence transformers and ChromaDB.
    
    Parameters
    ----------
    corpus : list of dict
        Each dict contains a 'text' field.
    collection_name : str
        Name of the ChromaDB collection.
    persist_dir : str
        Directory to persist the ChromaDB index.
    
    Returns
    -------
    tuple
        (chroma collection, model)
    """
    print("Loading sentence transformer model...")
    model = SentenceTransformer('all-MiniLM-L6-v2')

    print("Initializing ChromaDB...")
    client = chromadb.PersistentClient(path=persist_dir)
    
    # Delete collection if it already exists
    existing = [c.name for c in client.list_collections()]
    if collection_name in existing:
        client.delete_collection(collection_name)
    
    collection = client.create_collection(collection_name)

    print("Generating embeddings and indexing...")
    batch_size = 512
    for i in range(0, len(corpus), batch_size):
        batch = corpus[i:i+batch_size]
        texts = [doc['text'][:512] for doc in batch]
        ids = [str(doc['doc_id']) for doc in batch]
        metadatas = [
            {
                'asin': doc['asin'],
                'display_title': doc['display_title'][:200],
                'review_text': doc['review_text'][:200],
                'rating': float(doc['rating']) if doc['rating'] else 0.0
            }
            for doc in batch
        ]
        
        embeddings = model.encode(texts, show_progress_bar=False).tolist()
        collection.add(ids=ids, embeddings=embeddings, documents=texts, metadatas=metadatas)
        
        if i % 10000 == 0:
            print(f"Indexed {i}/{len(corpus)} documents...")

    print(f"Semantic index built: {collection.count()} documents")
    return collection, model

