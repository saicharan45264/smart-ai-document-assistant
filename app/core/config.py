import os

# Base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Folder where Chroma DB stores vectors
CHROMA_DIR = os.path.join(BASE_DIR, "db")

# Default Hugging Face model for answering queries
HF_MODEL = "google/flan-t5-base"

# Ensure the DB directory exists
os.makedirs(CHROMA_DIR, exist_ok=True)