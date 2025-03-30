from pydantic import BaseModel

class RetrievalRequest(BaseModel):
    query: str

class GraphRequest(BaseModel):
    query: str

class RagRequest(BaseModel):
    query: str
    rag_chunks: str
    graph_chunks: str
    temperature: float = 0.9