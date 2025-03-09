from config import CHUNK_OVERLAP_DEFAULT, CHUNK_SIZE_DEFAULT
from pydantic import BaseModel


class ChatRequest(BaseModel):
    query: str


class UploadConfig(BaseModel):
    chunk_size: int = CHUNK_SIZE_DEFAULT
    chunk_overlap: int = CHUNK_OVERLAP_DEFAULT
