# chat_models.py
# Description: Schemas and classes for chat messages and sessions
# Dependencies: pydantic
# Author: AI Generated Code
# Created: August 15, 2025

from pydantic import BaseModel
from typing import Optional

class ChatMessage(BaseModel):
    timestamp: str
    session_id: str
    user_id: str
    message_type: str    # 'user' or 'assistant'
    content: str
    document_ref: Optional[str] = ""
    response_time: Optional[float] = None
    model_used: Optional[str] = None
    tokens_used: Optional[int] = None
    confidence_score: Optional[float] = None