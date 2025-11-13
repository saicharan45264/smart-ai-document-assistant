# from langchain_community.vectorstores import Chroma
# from .embeddings import get_embedder
# import os

# CHROMA_DIR = os.environ.get("CHROMA_DIR", "./db/chroma")

# def create_vectorstore(chunks):
#     embedder = get_embedder()
#     texts = [d.page_content for d in chunks]
#     metadatas = [d.metadata for d in chunks]
#     db = Chroma.from_texts(texts, embedding=embedder, metadatas=metadatas, persist_directory=CHROMA_DIR)
#     db.persist()
#     return db

# # Simple getter for demo (loads existing)
# def get_existing_vectorstore():
#     if not os.path.exists(CHROMA_DIR):
#         return None
#     embedder = get_embedder()
#     db = Chroma(persist_directory=CHROMA_DIR, embedding_function=embedder.embed_query)
#     return db

import os
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Persistent directory for Chroma DB
CHROMA_DIR = os.getenv("CHROMA_DIR", "./db/chroma")

# ✅ Create new vectorstore from Document chunks
def create_vectorstore(chunks):
    embedder = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    # Extract plain text content and metadata from Documents
    texts = [doc.page_content for doc in chunks]
    metadatas = [doc.metadata for doc in chunks]

    db = Chroma.from_texts(
        texts=texts,
        embedding=embedder,
        metadatas=metadatas,
        persist_directory=CHROMA_DIR
    )
    db.persist()
    return db

# ✅ Get existing vectorstore (used when answering questions)
def get_existing_vectorstore():
    embedder = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    db = Chroma(
        persist_directory=CHROMA_DIR,
        embedding_function=embedder
    )
    return db