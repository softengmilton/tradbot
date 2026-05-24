import json
import uuid
from datetime import datetime, timedelta
from typing import Optional, Dict, List

class SessionStore:
    """In-memory session store (for Phase 2, upgrade to DB in Phase 3)"""

    def __init__(self):
        self.sessions = {}  # {session_id: session_data}
        self.timeout_minutes = 60

    def create_session(self, image_base64: str, analysis: str,
                       symbol: str = "Unknown") -> str:
        """Create new analysis session"""

        session_id = str(uuid.uuid4())
        self.sessions[session_id] = {
            "id": session_id,
            "created_at": datetime.now().isoformat(),
            "last_accessed": datetime.now().isoformat(),
            "image": image_base64,
            "analysis": analysis,
            "symbol": symbol,
            "messages": []
        }

        return session_id

    def get_session(self, session_id: str) -> Optional[Dict]:
        """Retrieve session by ID"""

        if session_id not in self.sessions:
            return None

        session = self.sessions[session_id]

        # Check timeout
        last_accessed = datetime.fromisoformat(session["last_accessed"])
        if datetime.now() - last_accessed > timedelta(minutes=self.timeout_minutes):
            del self.sessions[session_id]
            return None

        # Update last accessed
        session["last_accessed"] = datetime.now().isoformat()
        return session

    def add_message(self, session_id: str, role: str, content: str) -> bool:
        """Add message to session chat history"""

        session = self.sessions.get(session_id)
        if not session:
            return False

        session["messages"].append({
            "role": role,  # "user" or "assistant"
            "content": content,
            "timestamp": datetime.now().isoformat()
        })

        session["last_accessed"] = datetime.now().isoformat()
        return True

    def get_messages(self, session_id: str) -> Optional[List[Dict]]:
        """Get all messages in a session"""

        session = self.sessions.get(session_id)
        if not session:
            return None

        return session.get("messages", [])

    def cleanup_expired_sessions(self):
        """Remove expired sessions"""

        now = datetime.now()
        expired = []

        for sid, data in list(self.sessions.items()):
            last_accessed = datetime.fromisoformat(data["last_accessed"])
            if now - last_accessed > timedelta(minutes=self.timeout_minutes):
                expired.append(sid)

        for sid in expired:
            del self.sessions[sid]

        return len(expired)
