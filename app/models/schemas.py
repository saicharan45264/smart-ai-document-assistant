from pydantic import BaseModel

class UploadResponse(BaseModel):
    status: str
    indexed_chunks: int
    file: str

class ChatResponse(BaseModel):
    answer: str
    sources: list
