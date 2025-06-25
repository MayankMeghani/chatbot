import streamlit as st
import requests
import jwt
from datetime import datetime

API_URL = "https://chatbot-pct9.onrender.com"

# Initialize all session state variables at the very top
if 'access_token' not in st.session_state:
    st.session_state.access_token = None
    st.session_state.role = None
    st.session_state.username = None

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

if 'query_input' not in st.session_state:
    st.session_state.query_input = ""

st.set_page_config(page_title="FinSolve Chatbot", page_icon="💬", layout="wide")

def show_login():
    st.title("🔐 Login")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### Welcome to FinSolve Chatbot")
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        
        if st.button("Login", use_container_width=True):
            if username and password:
                try:
                    res = requests.post(
                        f"{API_URL}/login",
                        data={"username": username, "password": password},
                        headers={"Content-Type": "application/x-www-form-urlencoded"}
                    )
                    if res.status_code == 200:
                        token_data = res.json()
                        st.session_state.access_token = token_data["access_token"]
                        payload = jwt.decode(token_data["access_token"], "secret-key", algorithms=["HS256"])
                        st.session_state.role = payload["role"]
                        st.session_state.username = payload["sub"]
                        st.session_state.chat_history = []
                        st.success("Login successful!")
                        st.rerun()
                    else:
                        st.error("Login failed. Please check your credentials.")
                except Exception as e:
                    st.error(f"Connection error: {e}")
            else:
                st.warning("Please enter both username and password.")

def display_chat_history():
    if st.session_state.chat_history:
        st.markdown("### 💬 Chat History")
        chat_container = st.container()
        
        with chat_container:
            for chat in st.session_state.chat_history:
                st.markdown(f"""
                <div style="background-color: #f0f2f6; padding: 10px; border-radius: 10px; margin: 5px 0; margin-left: 20%;">
                    <strong>You:</strong> {chat['user_message']}
                    <br><small style="color: #666;">{chat['timestamp']}</small>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown(f"""
                <div style="background-color: #e8f5e8; padding: 10px; border-radius: 10px; margin: 5px 0; margin-right: 20%;">
                    <strong>🤖 FinSolve:</strong> {chat['bot_response']}
                </div>
                """, unsafe_allow_html=True)
                st.markdown("---")
    else:
        st.info("No chat history yet. Start a conversation!")

def show_chatbot():
    with st.sidebar:
        st.success(f"Logged in as **{st.session_state.username}**")
        st.info(f"Role: {st.session_state.role}")
        st.markdown("---")
        
        if st.button("🗑️ Clear Chat History", use_container_width=True):
            # Clear frontend memory
            st.session_state.chat_history = []

            # Clear backend memory
            try:
                response = requests.post(
                    f"{API_URL}/clear_memory",
                    headers={"Authorization": f"Bearer {st.session_state.access_token}"}
                )
                if response.status_code == 200:
                    st.success("Chat memory cleared.")
                else:
                    st.warning("Unable to clear backend memory.")
            except Exception as e:
                st.error(f"Backend error: {e}")

            st.rerun()

        
        if st.session_state.chat_history:
            chat_text = "\n\n".join(
                f"[{chat['timestamp']}]\nYou: {chat['user_message']}\nFinSolve: {chat['bot_response']}"
                for chat in st.session_state.chat_history
            )
            st.download_button(
                label="📥 Download Chat History",
                data=chat_text,
                file_name=f"finsolve_chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain",
                use_container_width=True
            )
        
        st.markdown("---")
        
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.access_token = None
            st.session_state.username = None
            st.session_state.role = None
            st.session_state.chat_history = []
            st.rerun()
    
    st.title("🤖 FinSolve Chatbot")
    st.markdown("Ask me anything about finance, investments, or financial planning!")
    
    # Create a form to properly handle the input submission
    with st.form("chat_form"):
        query = st.text_input(
            "Ask something:", 
            placeholder="Type your financial question here...", 
            key="query_input"
        )
        submitted = st.form_submit_button("📤 Send")
    
    if submitted and query:
        if query.strip():
            with st.spinner("🤔 Thinking..."):
                try:
                    response = requests.post(
                        f"{API_URL}/chatbot",
                        headers={
                            "Authorization": f"Bearer {st.session_state.access_token}",
                            "Content-Type": "application/json"
                        },
                        json={"query": query}
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        chat_entry = {
                            "user_message": query,
                            "bot_response": data["message"],
                            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        }
                        st.session_state.chat_history.append(chat_entry)
                        # Clear the input by using form submission behavior
                        st.rerun()
                    elif response.status_code == 401:
                        st.error("Session expired. Please login again.")
                        st.session_state.access_token = None
                        st.rerun()
                    else:
                        st.error(f"Error: {response.status_code} - {response.text}")
                except Exception as e:
                    st.error(f"Connection error: {e}")
        else:
            st.warning("Please enter a question.")
    
    st.markdown("---")
    display_chat_history()

def main():
    if st.session_state.access_token:
        show_chatbot()
    else:
        show_login()

if __name__ == "__main__":
    main()