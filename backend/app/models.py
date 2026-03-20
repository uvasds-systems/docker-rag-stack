from pydantic import BaseModel


class QueryRequest(BaseModel):
    question: str


class QueryResponse(BaseModel):
    answer: str
    sources: list[str]


class DocumentInfo(BaseModel):
    name: str
    size: int
    last_modified: str


class IngestResponse(BaseModel):
    filename: str
    chunks: int
    message: str
