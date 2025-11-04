# chat_service.py
# Description: Business logic for chat session and message handling
# Dependencies: backend/app/models/chat_models.py
# Author: AI Generated Code
# Created: August 15, 2025

from backend.app.models.chat_models import ChatMessage
from typing import List

class ChatService:
    """Business logic for chat operations."""
    def __init__(self):
        self.sessions = {}
    
    def add_message(self, session_id: str, message: ChatMessage):
        self.sessions.setdefault(session_id, []).append(message)
    
    def get_messages(self, session_id: str) -> List[ChatMessage]:
        return self.sessions.get(session_id, [])