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


def semantic_search(query, collection, model, top_k=5):
    """
    Search the semantic index for the given query.
    
    Parameters
    ----------
    query : str
        The search query.
    collection : chromadb collection
        The ChromaDB collection.
    model : SentenceTransformer
        The sentence transformer model.
    top_k : int
        Number of results to return.
    
    Returns
    -------
    list of dict
        Top k results with scores.
    """
    query_embedding = model.encode([query]).tolist()
    
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=top_k
    )
    
    output = []
    for i in range(len(results['ids'][0])):
        output.append({
            'doc_id': results['ids'][0][i],
            'display_title': results['metadatas'][0][i]['display_title'],
            'review_text': results['metadatas'][0][i]['review_text'],
            'rating': results['metadatas'][0][i]['rating'],
            'score': round(1 - results['distances'][0][i], 4)
        })
    
    return output

if __name__ == "__main__":
    import os

    reviews_path = os.path.join('data', 'raw', 'All_Beauty.jsonl')
    meta_path = os.path.join('data', 'raw', 'meta_All_Beauty.jsonl')

    # Load corpus
    corpus = load_corpus(reviews_path, meta_path)

    # Build index
    collection, model = build_semantic_index(corpus)

    # Test search
    query = "moisturizer for dry skin"
    results = semantic_search(query, collection, model, top_k=5)
    print(f"\nTop 5 results for: '{query}'")
    for i, r in enumerate(results):
        print(f"\n{i+1}. {r['display_title']}")
        print(f"   Score: {r['score']}")
        print(f"   Rating: {r['rating']}")



