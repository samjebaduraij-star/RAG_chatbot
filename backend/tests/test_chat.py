# test_chat.py
# Description: Pytest for chat operations
# Author: AI Generated Code
# Created: August 15, 2025

import pytest
from backend.app.services.chat_service import ChatService
from backend.app.models.chat_models import ChatMessage

def test_add_and_get_messages():
    service = ChatService()
    msg = ChatMessage(
        timestamp="2025-08-15T19:31:00",
        session_id="sess001",
        user_id="user1",
        message_type="user",
        content="Hello"
    )
    service.add_message("sess001", msg)
    msgs = service.get_messages("sess001")
    assert len(msgs) == 1
    assert msgs[0].content == "Hello"