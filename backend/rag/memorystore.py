from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.messages import SystemMessage
from langchain_core.messages import HumanMessage
from services.dummy_db import get_user

def get_initial_user_message(username: str, role: str) -> HumanMessage:
    return HumanMessage(
        content=(
            f"My name is {username}, and I belong to the '{role}' department.\n"
            f"Please consider my role-based access while responding to queries."
        )
    )

def get_system_message() -> SystemMessage:
    return SystemMessage(
    content=(
        "You are FinSolve’s secure AI assistant designed with enterprise-grade role-based access control (RBAC).\n\n"
        "Your primary goal is to provide accurate and helpful responses. Use the provided document context when available, "
        "especially for internal or sensitive topics. For general or external questions (e.g., communication tips, email writing, general HR advice), "
        "you may respond using your broader knowledge base.\n\n"

        "Roles and Access:\n"
        "- Finance: Financial reports, marketing expenses, equipment costs, reimbursements.\n"
        "- Marketing: Campaign performance, customer feedback, sales metrics.\n"
        "- HR: Employee data, attendance, payroll, performance reviews.\n"
        "- Engineering: Architecture, DevOps, processes, technical operations.\n"
        "- C-Level Executives: Access to all departments' data.\n"
        "- Employees: Only general company policies, FAQs, and events.\n\n"

        "Guidelines:\n"
        "- Prefer the provided context when available.\n"
        "- If a sensitive question has no relevant context, respond with: 'Access is restricted or information is not available for your role.'\n"
        "- For general-purpose or external queries, use your best judgment to assist.\n"
        "- When referencing internal documents, mention the source department clearly.\n\n"

        "Maintain clarity, professionalism, and accuracy at all times."
        )
    )



class MemoryStore:
    def __init__(self):
        self.sessions = {}

    def get_history(self, session_id: str) -> ChatMessageHistory:
        if session_id not in self.sessions:
            history = ChatMessageHistory()
            history.add_message(get_system_message())  
            role = get_user(session_id).get("role", "employee")
            history.add_message(get_initial_user_message(session_id, role))  
            self.sessions[session_id] = history
        return self.sessions[session_id]

    
    def reset_memory(self, session_id: str):
        if session_id in self.sessions:
            del self.sessions[session_id]

