# chat_interface.py

# Description: Streamlit chat interface component with message handling

# Dependencies: streamlit, typing, logging

# Author: AI Generated Code

# Created: August 09, 2025



import streamlit as st

import logging

from typing import List, Dict, Any, Optional

from datetime import datetime

import asyncio

import time



from ..core.chat_manager import ChatManager

from ..core.history_manager import HistoryManager



class ChatInterface:

    """Streamlit chat interface component."""

    

    def __init__(self, chat_manager: ChatManager, history_manager: HistoryManager):

        """Initialize chat interface.

        

        Args:

            chat_manager: Chat management service

            history_manager: History management service

        """

        self.chat_manager = chat_manager

        self.history_manager = history_manager

        self.logger = logging.getLogger(__name__)

    

    def render(self) -> None:

        """Render the chat interface."""

        try:

            # Display chat history

            self._display_chat_history()

            

            # Chat input

            self._render_chat_input()

            

            # Chat controls

            self._render_chat_controls()

            

        except Exception as e:

            self.logger.error(f"Chat interface render error: {e}")

            st.error(f"Chat interface error: {e}")

    

    def _display_chat_history(self) -> None:

        """Display chat message history."""

        messages = st.session_state.get("messages", [])

        

        # Create chat container

        chat_container = st.container()

        

        with chat_container:

            for message in messages:

                self._render_message(message)

    

    def _render_message(self, message: Dict[str, Any]) -> None:

        """Render a single chat message.

        

        Args:

            message: Message dictionary with role and content

        """

        role = message.get("role", "user")

        content = message.get("content", "")

        timestamp = message.get("timestamp", "")

        

        with st.chat_message(role):

            st.write(content)

            if timestamp:

                st.caption(f"🕒 {timestamp}")

    

    def _render_chat_input(self) -> None:

        """Render chat input field and handle user messages."""

        # Chat input

        if prompt := st.chat_input("Type your question here..."):

            self._handle_user_message(prompt)

    

    def _handle_user_message(self, message: str) -> None:

        """Handle user message input.

        

        Args:

            message: User input message

        """

        try:

            timestamp = datetime.now().strftime("%H:%M:%S")

            

            # Add user message to session

            user_message = {

                "role": "user",

                "content": message,

                "timestamp": timestamp

            }

            st.session_state.messages.append(user_message)

            

            # Display user message

            with st.chat_message("user"):

                st.write(message)

                st.caption(f"🕒 {timestamp}")

            

            # Generate AI response

            self._generate_ai_response(message)

            

            # Save to history

            self._save_message_history(user_message)

            

        except Exception as e:

            self.logger.error(f"Error handling user message: {e}")

            st.error(f"Error processing message: {e}")

    

    def _generate_ai_response(self, user_message: str) -> None:

        """Generate AI response to user message.

        

        Args:

            user_message: User's input message

        """

        try:

            with st.chat_message("assistant"):

                # Show typing indicator

                with st.spinner("🤔 Thinking..."):

                    start_time = time.time()

                    

                    # Get response from chat manager

                    response = self.chat_manager.get_response(

                        message=user_message,

                        session_id=st.session_state.chat_session_id,

                        user_id=st.session_state.user_id,

                        context_documents=st.session_state.processed_documents

                    )

                    

                    response_time = time.time() - start_time

                

                # Display response

                st.write(response["content"])

                timestamp = datetime.now().strftime("%H:%M:%S")

                st.caption(f"🕒 {timestamp} | ⏱️ {response_time:.2f}s")

                

                # Add to session messages

                assistant_message = {

                    "role": "assistant",

                    "content": response["content"],

                    "timestamp": timestamp,

                    "response_time": response_time,

                    "model_used": response.get("model_used", ""),

                    "tokens_used": response.get("tokens_used", 0)

                }

                st.session_state.messages.append(assistant_message)

                

                # Save to history

                self._save_message_history(assistant_message)

                

        except Exception as e:

            self.logger.error(f"Error generating AI response: {e}")

            st.error(f"Error generating response: {e}")

    

    def _save_message_history(self, message: Dict[str, Any]) -> None:

        """Save message to history.

        

        Args:

            message: Message dictionary to save

        """

        try:

            self.history_manager.add_message(

                session_id=st.session_state.chat_session_id,

                user_id=st.session_state.user_id,

                message_type=message["role"],

                content=message["content"],

                metadata={

                    "timestamp": message.get("timestamp", ""),

                    "response_time": message.get("response_time", 0.0),

                    "model_used": message.get("model_used", ""),

                    "tokens_used": message.get("tokens_used", 0)

                }

            )

        except Exception as e:

            self.logger.error(f"Error saving message history: {e}")

    

    def _render_chat_controls(self) -> None:

        """Render chat control buttons."""

        col1, col2, col3 = st.columns(3)

        

        with col1:

            if st.button("🗑️ Clear Chat", help="Clear current conversation"):

                self._clear_chat()

        

        with col2:

            if st.button("💾 Save Session", help="Save current session"):

                self._save_current_session()

        

        with col3:

            if st.button("📥 Export History", help="Export chat history"):

                self._export_chat_history()

    

    def _clear_chat(self) -> None:

        """Clear current chat session."""

        try:

            st.session_state.messages = []

            st.session_state.chat_session_id = self.history_manager.create_new_session()

            st.rerun()

        except Exception as e:

            self.logger.error(f"Error clearing chat: {e}")

            st.error(f"Error clearing chat: {e}")

    

    def _save_current_session(self) -> None:

        """Save current chat session."""

        try:

            self.history_manager.save_session(st.session_state.chat_session_id)

            st.success("💾 Session saved successfully!")

        except Exception as e:

            self.logger.error(f"Error saving session: {e}")

            st.error(f"Error saving session: {e}")

    

    def _export_chat_history(self) -> None:

        """Export chat history for download."""

        try:

            history_data = self.history_manager.export_history(

                session_id=st.session_state.chat_session_id

            )

            

            if history_data:

                st.download_button(

                    label="📥 Download History (TXT)",

                    data=history_data["txt"],

                    file_name=f"chat_history_{st.session_state.chat_session_id}.txt",

                    mime="text/plain"

                )

                

                st.download_button(

                    label="📊 Download History (CSV)",

                    data=history_data["csv"],

                    file_name=f"chat_history_{st.session_state.chat_session_id}.csv",

                    mime="text/csv"

                )

            else:

                st.warning("No chat history to export")

                

        except Exception as e:

            self.logger.error(f"Error exporting history: {e}")

            st.error(f"Error exporting history: {e}")