# chat.py
# Description: FastAPI endpoint for chat requests
# Dependencies: fastapi, shared.schemas, logging
# Author: AI Generated Code
# Created: August 15, 2025

from fastapi import APIRouter, HTTPException
from shared.schemas.common_schemas import ChatMessageSchema
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/chat", response_model=ChatMessageSchema)
async def chat_endpoint(message: ChatMessageSchema):
    try:
        logger.info(f"Received chat message {message.content}")
        # AI logic here: Call Gemini API via service layer (pseudo)
        response = message.copy(update={
            "message_type": "assistant",
            "content": f"Echo: {message.content}",
            "response_time": 0.0 # <simulate or measure>
        })
        return response
    except Exception as e:
        logger.error(f"Chat endpoint error: {e}")
        raise HTTPException(status_code=500, detail=str(e))