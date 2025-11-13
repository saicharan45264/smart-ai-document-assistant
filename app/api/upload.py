from fastapi import APIRouter, UploadFile, File, HTTPException
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
import os
import shutil
import chromadb # Import the full chromadb client

router = APIRouter()

CHROMA_PATH = "./db/chroma"
TEMP_DIR = "./temp"
# We must define a consistent collection name
COLLECTION_NAME = "university_docs"

@router.post("/pdf")
async def upload_pdf(file: UploadFile = File(...)):
    """
    Handles uploading a PDF file, processing it, and storing its
    embeddings in the Chroma vector store.
    """
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a PDF.")

    os.makedirs(TEMP_DIR, exist_ok=True)
    temp_file_path = os.path.join(TEMP_DIR, file.filename)

    try:
        # Save the uploaded file temporarily
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        print(f"[+] File saved temporarily to: {temp_file_path}")

        # 1. Load the PDF
        loader = PyPDFLoader(temp_file_path)
        documents = loader.load()

        if not documents:
            raise HTTPException(status_code=400, detail="Could not load any content from the PDF.")
            
        print(f"[+] PDF loaded. {len(documents)} page(s) found.")

        # 2. Split the text into chunks
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = text_splitter.split_documents(documents)
        print(f"[+] Document split into {len(chunks)} chunks.")

        # 3. Initialize embeddings
        embeddings = OllamaEmbeddings(model="nomic-embed-text")

        # --- REVISED DATABASE LOGIC (THE FIX) ---
        # We no longer use shutil.rmtree.
        # We use the Chroma client to manage the collection.

        # 4. Initialize a persistent ChromaDB client
        client = chromadb.PersistentClient(path=CHROMA_PATH)

        # 5. Clear the old collection if it exists
        try:
            # Check if collection exists before deleting
            collections = client.list_collections()
            if any(c.name == COLLECTION_NAME for c in collections):
                print(f"[+] Clearing old collection: {COLLECTION_NAME}")
                client.delete_collection(name=COLLECTION_NAME)
        except Exception as e:
            print(f"[Warning] Error clearing collection (this might be ok if it's the first run): {e}")

        # 6. Create a new collection
        # We pass the *client* to the Chroma wrapper
        db = Chroma(
            client=client,
            collection_name=COLLECTION_NAME,
            embedding_function=embeddings,
        )

        print(f"[+] Adding {len(chunks)} new document chunks...")
        # Add documents to the new collection
        db.add_documents(chunks)
        
        # --- THIS IS THE FIX ---
        # The line `db.persist()` was here. It's now removed.
        # The PersistentClient handles persistence automatically.
        
        print(f"[+] Vector store created/updated and persisted at {CHROMA_PATH}.")

        return {"message": f"Successfully uploaded and indexed '{file.filename}'."}

    except Exception as e:
        print(f"[Error in /upload/pdf] {str(e)}")
        # This will now show the *real* error if it's not the 'readonly' one
        raise HTTPException(status_code=500, detail=f"Failed to process PDF: {str(e)}")
        
    finally:
        # Clean up the temporary file
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
            print(f"[-] Temporary file {temp_file_path} removed.")
        await file.close()