from langchain_community.chat_message_histories import ChatMessageHistory

class MemoryStore:
    def __init__(self):
        self.sessions = {}

    def get_history(self, session_id: str) -> ChatMessageHistory:
        if session_id not in self.sessions:
            self.sessions[session_id] = ChatMessageHistory()
        return self.sessions[session_id]
    
    def reset_memory(self, session_id: str):
        if session_id in self.sessions:
            del self.sessions[session_id]

