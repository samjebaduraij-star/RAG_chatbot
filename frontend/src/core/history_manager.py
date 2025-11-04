# history_manager.py
# Description: Chat history management with dual storage formats
# Dependencies: json, csv, pathlib, typing
# Author: AI Generated Code
# Created: August 12, 2025

import json
import csv
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timedelta
import uuid
import os

class HistoryManager:
    """Manages chat history storage in both TXT and CSV formats."""
    
    def __init__(self):
        """Initialize history manager."""
        self.logger = logging.getLogger(__name__)
        
        # Storage paths
        self.history_dir = Path("frontend/data/chat_history")
        self.sessions_dir = self.history_dir / "sessions"
        self.exports_dir = self.history_dir / "exports"
        
        # Create directories
        self.history_dir.mkdir(parents=True, exist_ok=True)
        self.sessions_dir.mkdir(parents=True, exist_ok=True)
        self.exports_dir.mkdir(parents=True, exist_ok=True)
        
        # File paths
        self.txt_log_file = self.history_dir / "chat_log.txt"
        self.csv_log_file = self.history_dir / "chat_log.csv"
        self.sessions_index_file = self.history_dir / "sessions_index.json"
        
        # Initialize CSV file if it doesn't exist
        self._initialize_csv_file()
    
    def create_new_session(self) -> str:
        """Create a new chat session.
        
        Returns:
            New session identifier
        """
        try:
            session_id = str(uuid.uuid4())[:8]
            timestamp = datetime.now().isoformat()
            
            # Create session metadata
            session_info = {
                "session_id": session_id,
                "created_at": timestamp,
                "last_activity": timestamp,
                "message_count": 0,
                "user_id": "default_user"
            }
            
            # Save session info
            self._save_session_info(session_info)
            
            self.logger.info(f"Created new session: {session_id}")
            return session_id
            
        except Exception as e:
            self.logger.error(f"Error creating new session: {e}")
            return str(uuid.uuid4())[:8]  # Fallback
    
    def add_message(
        self,
        session_id: str,
        user_id: str,
        message_type: str,
        content: str,
        metadata: Dict[str, Any] = None
    ) -> None:
        """Add message to chat history.
        
        Args:
            session_id: Chat session identifier
            user_id: User identifier
            message_type: Type of message ('user' or 'assistant')
            content: Message content
            metadata: Additional message metadata
        """
        try:
            timestamp = datetime.now().isoformat()
            metadata = metadata or {}
            
            # Create message entry
            message = {
                "timestamp": timestamp,
                "session_id": session_id,
                "user_id": user_id,
                "message_type": message_type,
                "content": content,
                "document_ref": metadata.get("document_ref", ""),
                "response_time": metadata.get("response_time", 0.0),
                "model_used": metadata.get("model_used", ""),
                "tokens_used": metadata.get("tokens_used", 0),
                "confidence_score": metadata.get("confidence_score", 0.0)
            }
            
            # Save to both formats
            self._save_to_txt(message)
            self._save_to_csv(message)
            self._save_to_session_file(session_id, message)
            
            # Update session info
            self._update_session_activity(session_id)
            
        except Exception as e:
            self.logger.error(f"Error adding message to history: {e}")
    
    def _save_to_txt(self, message: Dict[str, Any]) -> None:
        """Save message to TXT format (tab-separated).
        
        Args:
            message: Message data to save
        """
        try:
            # Format: timestamp\tuser_id\tsession_id\tmessage_type\tcontent\tdocument_ref\tresponse_time
            txt_line = "\t".join([
                message["timestamp"],
                message["user_id"],
                message["session_id"],
                message["message_type"],
                message["content"].replace("\n", "\\n").replace("\t", "\\t"),
                message["document_ref"],
                str(message["response_time"])
            ]) + "\n"
            
            # Append to TXT file
            with open(self.txt_log_file, 'a', encoding='utf-8') as file:
                file.write(txt_line)
                
        except Exception as e:
            self.logger.error(f"Error saving to TXT: {e}")
    
    def _save_to_csv(self, message: Dict[str, Any]) -> None:
        """Save message to CSV format.
        
        Args:
            message: Message data to save
        """
        try:
            # Write to CSV file
            with open(self.csv_log_file, 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([
                    message["timestamp"],
                    message["user_id"],
                    message["session_id"],
                    message["message_type"],
                    message["content"],
                    message["document_ref"],
                    message["response_time"],
                    message["model_used"],
                    message["tokens_used"],
                    message["confidence_score"]
                ])
                
        except Exception as e:
            self.logger.error(f"Error saving to CSV: {e}")
    
    def _save_to_session_file(self, session_id: str, message: Dict[str, Any]) -> None:
        """Save message to individual session file.
        
        Args:
            session_id: Session identifier
            message: Message data to save
        """
        try:
            session_file = self.sessions_dir / f"{session_id}.json"
            
            # Load existing messages
            messages = []
            if session_file.exists():
                with open(session_file, 'r', encoding='utf-8') as file:
                    messages = json.load(file)
            
            # Add new message
            messages.append(message)
            
            # Save updated messages
            with open(session_file, 'w', encoding='utf-8') as file:
                json.dump(messages, file, indent=2, ensure_ascii=False)
                
        except Exception as e:
            self.logger.error(f"Error saving to session file: {e}")
    
    def _initialize_csv_file(self) -> None:
        """Initialize CSV file with headers if it doesn't exist."""
        try:
            if not self.csv_log_file.exists():
                headers = [
                    "timestamp", "user_id", "session_id", "message_type", "content",
                    "document_ref", "response_time", "model_used", "tokens_used", "confidence_score"
                ]
                
                with open(self.csv_log_file, 'w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow(headers)
                    
        except Exception as e:
            self.logger.error(f"Error initializing CSV file: {e}")
    
    def _save_session_info(self, session_info: Dict[str, Any]) -> None:
        """Save session information to index.
        
        Args:
            session_info: Session metadata
        """
        try:
            # Load existing sessions
            sessions = []
            if self.sessions_index_file.exists():
                with open(self.sessions_index_file, 'r', encoding='utf-8') as file:
                    sessions = json.load(file)
            
            # Add new session
            sessions.append(session_info)
            
            # Save updated sessions
            with open(self.sessions_index_file, 'w', encoding='utf-8') as file:
                json.dump(sessions, file, indent=2, ensure_ascii=False)
                
        except Exception as e:
            self.logger.error(f"Error saving session info: {e}")
    
    def _update_session_activity(self, session_id: str) -> None:
        """Update session last activity timestamp.
        
        Args:
            session_id: Session identifier
        """
        try:
            if not self.sessions_index_file.exists():
                return
            
            # Load sessions
            with open(self.sessions_index_file, 'r', encoding='utf-8') as file:
                sessions = json.load(file)
            
            # Update session
            for session in sessions:
                if session["session_id"] == session_id:
                    session["last_activity"] = datetime.now().isoformat()
                    session["message_count"] = session.get("message_count", 0) + 1
                    break
            
            # Save updated sessions
            with open(self.sessions_index_file, 'w', encoding='utf-8') as file:
                json.dump(sessions, file, indent=2, ensure_ascii=False)
                
        except Exception as e:
            self.logger.error(f"Error updating session activity: {e}")
    
    def get_session_list(self) -> List[str]:
        """Get list of available sessions.
        
        Returns:
            List of session identifiers
        """
        try:
            if not self.sessions_index_file.exists():
                return []
            
            with open(self.sessions_index_file, 'r', encoding='utf-8') as file:
                sessions = json.load(file)
            
            # Sort by last activity (most recent first)
            sessions.sort(key=lambda x: x.get("last_activity", ""), reverse=True)
            
            return [session["session_id"] for session in sessions]
            
        except Exception as e:
            self.logger.error(f"Error getting session list: {e}")
            return []
    
    def load_session(self, session_id: str) -> List[Dict[str, Any]]:
        """Load messages from a specific session.
        
        Args:
            session_id: Session identifier to load
        
        Returns:
            List of messages in the session
        """
        try:
            session_file = self.sessions_dir / f"{session_id}.json"
            
            if not session_file.exists():
                return []
            
            with open(session_file, 'r', encoding='utf-8') as file:
                messages = json.load(file)
            
            # Convert to Streamlit chat format
            chat_messages = []
            for msg in messages:
                chat_messages.append({
                    "role": msg["message_type"],
                    "content": msg["content"],
                    "timestamp": msg["timestamp"]
                })
            
            return chat_messages
            
        except Exception as e:
            self.logger.error(f"Error loading session: {e}")
            return []
    
    def save_session(self, session_id: str) -> bool:
        """Explicitly save current session.
        
        Args:
            session_id: Session identifier
        
        Returns:
            True if saved successfully, False otherwise
        """
        try:
            # Session is automatically saved with each message
            # This method can be used for explicit saves or checkpoints
            self._update_session_activity(session_id)
            return True
            
        except Exception as e:
            self.logger.error(f"Error saving session: {e}")
            return False
    
    def export_history(self, session_id: str = None) -> Dict[str, str]:
        """Export chat history for download.
        
        Args:
            session_id: Optional session ID to export (exports all if None)
        
        Returns:
            Dictionary with 'txt' and 'csv' formatted data
        """
        try:
            if session_id:
                # Export specific session
                messages = self._get_session_messages(session_id)
            else:
                # Export all history
                messages = self._get_all_messages()
            
            if not messages:
                return {"txt": "", "csv": ""}
            
            # Generate TXT export
            txt_content = self._generate_txt_export(messages)
            
            # Generate CSV export
            csv_content = self._generate_csv_export(messages)
            
            return {
                "txt": txt_content,
                "csv": csv_content
            }
            
        except Exception as e:
            self.logger.error(f"Error exporting history: {e}")
            return {"txt": "", "csv": ""}
    
    def _get_session_messages(self, session_id: str) -> List[Dict[str, Any]]:
        """Get all messages from a specific session.
        
        Args:
            session_id: Session identifier
        
        Returns:
            List of messages
        """
        try:
            session_file = self.sessions_dir / f"{session_id}.json"
            
            if not session_file.exists():
                return []
            
            with open(session_file, 'r', encoding='utf-8') as file:
                return json.load(file)
                
        except Exception as e:
            self.logger.error(f"Error getting session messages: {e}")
            return []
    
    def _get_all_messages(self) -> List[Dict[str, Any]]:
        """Get all messages from all sessions.
        
        Returns:
            List of all messages
        """
        try:
            all_messages = []
            
            # Read from CSV file
            if self.csv_log_file.exists():
                with open(self.csv_log_file, 'r', encoding='utf-8') as file:
                    reader = csv.DictReader(file)
                    all_messages = list(reader)
            
            return all_messages
            
        except Exception as e:
            self.logger.error(f"Error getting all messages: {e}")
            return []
    
    def _generate_txt_export(self, messages: List[Dict[str, Any]]) -> str:
        """Generate TXT format export.
        
        Args:
            messages: List of messages to export
        
        Returns:
            TXT formatted string
        """
        try:
            txt_lines = []
            txt_lines.append("# Chat History Export (Tab-separated format)")
            txt_lines.append("# Format: timestamp\tuser_id\tsession_id\tmessage_type\tcontent\tdocument_ref\tresponse_time")
            txt_lines.append("")
            
            for msg in messages:
                line = "\t".join([
                    msg.get("timestamp", ""),
                    msg.get("user_id", ""),
                    msg.get("session_id", ""),
                    msg.get("message_type", ""),
                    msg.get("content", "").replace("\n", "\\n").replace("\t", "\\t"),
                    msg.get("document_ref", ""),
                    str(msg.get("response_time", 0.0))
                ])
                txt_lines.append(line)
            
            return "\n".join(txt_lines)
            
        except Exception as e:
            self.logger.error(f"Error generating TXT export: {e}")
            return ""
    
    def _generate_csv_export(self, messages: List[Dict[str, Any]]) -> str:
        """Generate CSV format export.
        
        Args:
            messages: List of messages to export
        
        Returns:
            CSV formatted string
        """
        try:
            from io import StringIO
            
            output = StringIO()
            writer = csv.writer(output)
            
            # Write headers
            headers = [
                "timestamp", "user_id", "session_id", "message_type", "content",
                "document_ref", "response_time", "model_used", "tokens_used", "confidence_score"
            ]
            writer.writerow(headers)
            
            # Write data
            for msg in messages:
                writer.writerow([
                    msg.get("timestamp", ""),
                    msg.get("user_id", ""),
                    msg.get("session_id", ""),
                    msg.get("message_type", ""),
                    msg.get("content", ""),
                    msg.get("document_ref", ""),
                    msg.get("response_time", 0.0),
                    msg.get("model_used", ""),
                    msg.get("tokens_used", 0),
                    msg.get("confidence_score", 0.0)
                ])
            
            return output.getvalue()
            
        except Exception as e:
            self.logger.error(f"Error generating CSV export: {e}")
            return ""
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get chat history statistics.
        
        Returns:
            Statistics dictionary
        """
        try:
            stats = {
                "total_sessions": 0,
                "total_messages": 0,
                "avg_messages": 0,
                "total_documents": 0
            }
            
            # Count sessions
            if self.sessions_index_file.exists():
                with open(self.sessions_index_file, 'r', encoding='utf-8') as file:
                    sessions = json.load(file)
                    stats["total_sessions"] = len(sessions)
                    
                    if sessions:
                        total_msg_count = sum(s.get("message_count", 0) for s in sessions)
                        stats["total_messages"] = total_msg_count
                        stats["avg_messages"] = round(total_msg_count / len(sessions), 1)
            
            # Count processed documents
            doc_index_file = Path("frontend/data/processed/document_index.json")
            if doc_index_file.exists():
                with open(doc_index_file, 'r', encoding='utf-8') as file:
                    documents = json.load(file)
                    stats["total_documents"] = len(documents)
            
            return stats
            
        except Exception as e:
            self.logger.error(f"Error getting statistics: {e}")
            return {"total_sessions": 0, "total_messages": 0, "avg_messages": 0, "total_documents": 0}
    
    def cleanup_old_sessions(self, days: int = 30) -> int:
        """Clean up old chat sessions.
        
        Args:
            days: Number of days to keep sessions
        
        Returns:
            Number of sessions removed
        """
        try:
            cutoff_date = datetime.now() - timedelta(days=days)
            removed_count = 0
            
            if not self.sessions_index_file.exists():
                return 0
            
            # Load sessions
            with open(self.sessions_index_file, 'r', encoding='utf-8') as file:
                sessions = json.load(file)
            
            # Filter old sessions
            active_sessions = []
            for session in sessions:
                last_activity = datetime.fromisoformat(session.get("last_activity", ""))
                
                if last_activity > cutoff_date:
                    active_sessions.append(session)
                else:
                    # Remove session file
                    session_file = self.sessions_dir / f"{session['session_id']}.json"
                    if session_file.exists():
                        session_file.unlink()
                    removed_count += 1
            
            # Save updated sessions
            with open(self.sessions_index_file, 'w', encoding='utf-8') as file:
                json.dump(active_sessions, file, indent=2, ensure_ascii=False)
            
            return removed_count
            
        except Exception as e:
            self.logger.error(f"Error cleaning up sessions: {e}")
            return 0
    
    def reset_all_data(self) -> None:
        """Reset all chat history data."""
        try:
            # Remove all files
            if self.txt_log_file.exists():
                self.txt_log_file.unlink()
            
            if self.csv_log_file.exists():
                self.csv_log_file.unlink()
            
            if self.sessions_index_file.exists():
                self.sessions_index_file.unlink()
            
            # Remove session files
            for session_file in self.sessions_dir.glob("*.json"):
                session_file.unlink()
            
            # Reinitialize
            self._initialize_csv_file()
            
            self.logger.info("All chat history data has been reset")
            
        except Exception as e:
            self.logger.error(f"Error resetting data: {e}")
            raise