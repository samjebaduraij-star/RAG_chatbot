# document_models.py
# Description: Schemas and classes for documents and their chunks
# Dependencies: pydantic
# Author: AI Generated Code
# Created: August 15, 2025

from pydantic import BaseModel
from typing import List, Dict, Any

class DocumentChunk(BaseModel):
    id: int
    content: str
    length: int
    sentence_count: int
    start_position: int
    end_position: int

class Document(BaseModel):
    id: str
    filename: str
    file_type: str
    processed_at: str
    metadata: Dict[str, Any]
    chunks: List[DocumentChunk]
    chunk_count: int
    total_characters: int
    total_words: int