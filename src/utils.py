import json
import re
import os
import pickle
from tqdm import tqdm


def preprocess_text(text):
    """Lowercase, remove punctuation, strip extra whitespace."""
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def join_list_field(field):
    """Join list fields into a single string."""
    if isinstance(field, list):
        return ' '.join([str(i) for i in field])
    return str(field) if field else ""


def load_corpus(reviews_path, meta_path, max_rows=None):
    """
    Load and combine reviews and metadata into a single corpus.
    
    Parameters
    ----------
    reviews_path : str
        Path to the reviews JSONL file.
    meta_path : str
        Path to the metadata JSONL file.
    max_rows : int, optional
        Maximum number of rows to load from each file.
    
    Returns
    -------
    list of dict
        Each dict contains: doc_id, text, title, rating, asin
    """
    # Load metadata into a dict keyed by parent_asin
    print("Loading metadata...")
    meta_lookup = {}
    with open(meta_path, 'r') as f:
        for i, line in enumerate(tqdm(f)):
            if max_rows and i >= max_rows:
                break
            record = json.loads(line)
            asin = record.get('parent_asin', '')
            title = preprocess_text(record.get('title', ''))
            features = preprocess_text(join_list_field(record.get('features', [])))
            description = preprocess_text(join_list_field(record.get('description', [])))
            meta_lookup[asin] = {
                'meta_title': title,
                'features': features,
                'description': description
            }

    # Load reviews and combine with metadata
    print("Loading reviews...")
    corpus = []
    with open(reviews_path, 'r') as f:
        for i, line in enumerate(tqdm(f)):
            if max_rows and i >= max_rows:
                break
            record = json.loads(line)
            asin = record.get('asin', '')
            review_title = preprocess_text(record.get('title', ''))
            review_text = preprocess_text(record.get('text', ''))
            rating = record.get('rating', None)

            # Get metadata for this product if available
            meta = meta_lookup.get(asin, {})
            meta_title = meta.get('meta_title', '')
            features = meta.get('features', '')
            description = meta.get('description', '')

            # Combine all text fields
            combined = ' '.join(filter(None, [
                meta_title, features, description, review_title, review_text
            ]))

            corpus.append({
                'doc_id': i,
                'asin': asin,
                'text': combined,
                'display_title': meta_title or review_title,
                'review_text': review_text,
                'rating': rating
            })

    print(f"Corpus built: {len(corpus)} documents")
    return corpus

def save_pickle(obj, path):
    """Save an object to a pickle file."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'wb') as f:
        pickle.dump(obj, f)
    print(f"Saved to {path}")


def load_pickle(path):
    """Load an object from a pickle file."""
    with open(path, 'rb') as f:
        obj = pickle.load(f)
    print(f"Loaded from {path}")
    return obj