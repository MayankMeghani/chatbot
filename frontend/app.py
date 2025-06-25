import streamlit as st
import requests
import jwt
from datetime import datetime

API_URL = st.secrets["api"].get("base_url", "http://localhost:8000")

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
    st.title("🔐 Login / Sign Up")
    
    tab_login, tab_signup = st.tabs(["Login", "Sign Up"])

    with tab_login:
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")
        
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
                        st.error("Login failed. Check credentials.")
                except Exception as e:
                    st.error(f"Connection error: {e}")
            else:
                st.warning("Enter both username and password.")

    with tab_signup:
        new_username = st.text_input("New Username", key="signup_username")
        new_password = st.text_input("New Password", type="password", key="signup_password")
        department = st.selectbox("Select Department", [
            "finance", "marketing", "hr", "engineering", "C-Level", "employee"
        ])

        if st.button("Create Account", use_container_width=True):
            if new_username and new_password:
                try:
                    res = requests.post(
                        f"{API_URL}/signup",
                        json={
                            "username": new_username,
                            "password": new_password,
                            "role": department
                        }
                    )
                    if res.status_code == 200:
                        st.success("Account created! You can now login.")
                    elif res.status_code == 409:
                        st.error("Username already exists.")
                    else:
                        st.error("Signup failed.")
                except Exception as e:
                    st.error(f"Signup error: {e}")
            else:
                st.warning("All fields are required.")

def show_chatbot():
    st.title("🤖 FinSolve Chatbot")

    # Sidebar
    with st.sidebar:
        st.success(f"Logged in as **{st.session_state.username}**")
        st.info(f"Role: {st.session_state.role}")
        st.markdown("---")

        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.chat_history = []
            try:
                requests.post(
                    f"{API_URL}/clear_memory",
                    headers={"Authorization": f"Bearer {st.session_state.access_token}"}
                )
                st.success("Chat memory cleared.")
            except Exception as e:
                st.error(f"Error clearing memory: {e}")
            st.rerun()

        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.clear()
            st.rerun()

        if st.session_state.chat_history:
            chat_text = "\n\n".join(
                f"[{chat['timestamp']}]\nYou: {chat['user_message']}\nFinSolve: {chat['bot_response']}"
                for chat in st.session_state.chat_history
            )
            st.download_button(
                "📥 Download Chat",
                chat_text,
                file_name=f"chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain",
                use_container_width=True
            )

    # 💬 Display chat messages
    for chat in st.session_state.chat_history:
        with st.chat_message("user"):
            st.markdown(chat["user_message"])
        with st.chat_message("assistant"):
            st.markdown(chat["bot_response"])

    # ⌨️ Chat input box (always at bottom)
    if prompt := st.chat_input("Type your message..."):
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.spinner("💬 Thinking..."):
            try:
                response = requests.post(
                    f"{API_URL}/chatbot",
                    headers={
                        "Authorization": f"Bearer {st.session_state.access_token}",
                        "Content-Type": "application/json"
                    },
                    json={"query": prompt}
                )

                if response.status_code == 200:
                    data = response.json()
                    reply = data["message"]
                    st.session_state.chat_history.append({
                        "user_message": prompt,
                        "bot_response": reply,
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })
                    with st.chat_message("assistant"):
                        st.markdown(reply)
                elif response.status_code == 401:
                    st.error("Session expired. Please log in again.")
                    st.session_state.clear()
                    st.rerun()
                else:
                    st.error(f"Server error: {response.status_code} - {response.text}")
            except Exception as e:
                st.error(f"Connection error: {e}")


def main():
    if st.session_state.access_token:
        show_chatbot()
    else:
        show_login()

if __name__ == "__main__":
    main()