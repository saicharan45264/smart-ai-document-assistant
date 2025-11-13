from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
import os

load_dotenv()

def get_embedder():
    # Use OpenAI Embeddings; change model name if needed
    api_key = os.environ.get('OPENAI_API_KEY')
    if not api_key:
        raise ValueError("OPENAI_API_KEY not set in environment")
    return OpenAIEmbeddings(model='text-embedding-3-small')
