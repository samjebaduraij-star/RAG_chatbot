# history.py

# Description: FastAPI endpoints for retrieving chat history

# Dependencies: backend/app/models/chat_models.py

# Author: AI Generated Code

# Created: August 15, 2025



from fastapi import APIRouter

from backend.app.services.chat_service import ChatService



router = APIRouter()

chat_service = ChatService()



@router.get("/history/{session_id}")

async def get_history(session_id: str):

    messages = chat_service.get_messages(session_id)

    return messages