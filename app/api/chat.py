from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain.chains import RetrievalQA
from langchain_community.llms import Ollama
import os

router = APIRouter()

CHROMA_PATH = "./db/chroma"

class Query(BaseModel):
    query: str

@router.post("/query")
async def query_ollama(input: Query):
    """
    Handles a user query by retrieving relevant context from the
    vector store and generating a response using the LLM.
    """
    try:
        print(f"[User query] {input.query}")

        # Initialize embeddings
        embeddings = OllamaEmbeddings(model="nomic-embed-text")

        # Check if vectorstore exists
        if not os.path.exists(CHROMA_PATH):
            print("[Error] No document index found.")
            raise HTTPException(status_code=400, detail="No document index found. Please upload a PDF first.")
        
        print("[+] Loading existing vector store...")
        db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)

        # Initialize the LLM
        llm = Ollama(model="llama3")

        # Create the retriever
        retriever = db.as_retriever(search_kwargs={"k": 3}) # Get top 3 results
        
        # Create the QA chain
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm, 
            retriever=retriever,
            chain_type="stuff" # "stuff" is a simple and common chain type
        )

        # Get the result
        # Note: .run() is deprecated. Use .invoke()
        result = qa_chain.invoke(input.query)
        
        # The result from .invoke() is often a dictionary. Let's get the 'result' key.
        response_text = result.get('result', 'No answer found.')

        print(f"[Response] {response_text}")

        return {"response": response_text}

    except Exception as e:
        print(f"[Error in /chat/query] {str(e)}")
        raise HTTPException(status_code=500, detail=f"Query failed: {str(e)}")