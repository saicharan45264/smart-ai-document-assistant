🚀 Smart University Assistant

AI-powered document analysis, intelligent query answering, and academic support system built using FastAPI, Next.js, LangChain, ChromaDB, and OpenAI.

This project allows students & faculty to upload university handbooks, PDFs, notices, or academic documents and ask natural language questions, receiving accurate answers backed by retrieval-augmented generation (RAG).

⸻

⭐ Features
	•	📄 PDF & Document Uploading (supports PDFs, text files, etc.)
	•	🧩 Automatic Text Extraction using PyPDF
	•	🔍 Semantic Search with Chroma Vector DB
	•	🧠 RAG Pipeline using LangChain
	•	🤖 LLM-powered Chat Interface (OpenAI / Gemini / any LLM)
	•	⚡ Real-time Responses through FastAPI API
	•	💻 Modern Frontend using Next.js + TailwindCSS
	•	🏗️ Modular & Extensible Architecture

⸻

🏛️ Tech Stack

Backend
	•	FastAPI
	•	LangChain
	•	ChromaDB
	•	PyPDF
	•	OpenAI API
	•	Uvicorn

Frontend
	•	Next.js
	•	React
	•	Tailwind CSS


🧬 Architecture Overview

User → Next.js Frontend → FastAPI Backend → 
PDF Processing → Chunking → Embeddings → ChromaDB →
RAG Pipeline → LLM → Response → Frontend Chat UI


Flow
	1.	User uploads a document
	2.	Backend extracts text & chunks it
	3.	Embeddings generated via LangChain
	4.	Stored in Chroma vectorstore
	5.	User asks question
	6.	Relevant chunks retrieved
	7.	Sent to LLM for answer


⚙️ Backend Setup

1. Create virtual environment:

python3 -m venv .venv
source .venv/bin/activate


2. Install dependencies:

pip install -r requirements.txt

3. Run backend

uvicorn app.main:app --reload

API will be available at: 
http://127.0.0.1:8000
http://127.0.0.1:8000/docs


💻 Frontend Setup:

1. Navigate to frontend: cd sua-frontend
2. 2. Install dependencies: npm install
3. npm run dev
Frontend will run at: http://localhost:3000



📄 Project Structure:

smart-ai-document-assistant/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── chat.py
│   │   │   ├── upload.py
│   │   ├── core/
│   │   ├── models/
│   │   ├── utils/
│   │   └── main.py
│   ├── db/
│   └── requirements.txt
│
├── sua-frontend/
│   ├── pages/
│   ├── styles/
│   ├── components/
│   ├── public/
│   ├── package.json
│   └── next.config.js
│
└── README.md



🧪 API Endpoints

POST /upload

Upload PDF → stores embeddings in Chroma.

POST /chat

Ask a question → backend retrieves context → LLM generates answer.

⸻

🛠️ Customization

You can easily modify:
	•	Embedding model
	•	LLM model (OpenAI, Gemini, Ollama, Llama, etc.)
	•	Chunk size
	•	Prompt format
	•	Retrieval parameters
	•	Frontend UI

⸻

🎯 Use Cases
	•	University handbook search
	•	Exam rule lookup
	•	Course catalog Q&A
	•	Department document search
	•	Policy-based intelligent question answering

⸻

🤝 Contributions

Pull requests and feature improvements are welcome.
