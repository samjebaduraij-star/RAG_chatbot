# common_schemas.py

# Description: Shared pydantic schemas for data validation

# Dependencies: pydantic

# Author: AI Generated Code

# Created: August 15, 2025



from pydantic import BaseModel, Field

from typing import Optional, List



class ChatMessageSchema(BaseModel):

    timestamp: str

    user_id: str

    session_id: str

    message_type: str

    content: str

    document_ref: Optional[str] = ''

    response_time: Optional[float] = None

    model_used: Optional[str] = ''

    tokens_used: Optional[int] = None

    confidence_score: Optional[float] = None



class DocumentSchema(BaseModel):

    id: str

    filename: str

    file_type: str

    processed_at: str

    metadata: dict

    chunks: List[dict]

    chunk_count: int

    total_characters: int

    total_words: int



# Additional schemas as needed...