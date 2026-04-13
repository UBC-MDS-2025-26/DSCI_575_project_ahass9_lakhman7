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