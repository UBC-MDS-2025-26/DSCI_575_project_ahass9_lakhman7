import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from groq import Groq
from dotenv import load_dotenv
from src.bm25 import bm25_search, tokenize
from src.rag_pipeline import semantic_retriever, build_context, build_prompt

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))