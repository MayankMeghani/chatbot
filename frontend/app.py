import streamlit as st
import requests
from jose import jwt

API_URL = "http://127.0.0.1:8000"

# Initialize session state variables at the very top
if 'access_token' not in st.session_state:
    st.session_state.access_token = None
    st.session_state.role = None
    st.session_state.username = None

st.set_page_config(page_title="FinSolve Chatbot", page_icon="💬")

def show_login():
    st.title("🔐 Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
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
                st.rerun()  # Critical - forces full script rerun with new session state
            else:
                st.error("Login failed. Please check credentials.")
        except Exception as e:
            st.error(f"Error: {e}")

def show_chatbot():
    st.sidebar.success(f"Logged in as {st.session_state.username} ({st.session_state.role})")
    st.title("🤖 FinSolve Chatbot")
    
    query = st.text_input("Ask something:")
    if st.button("Submit") and query:
        try:
            response = requests.get(
                f"{API_URL}/engineering-data",
                headers={"Authorization": f"Bearer {st.session_state.access_token}"}
            )
            if response.status_code == 200:
                data = response.json()
                st.success(data["message"])
            else:
                st.error(f"Access denied: {response.status_code}")
        except Exception as e:
            st.error(f"Error: {e}")
    
    if st.button("Logout"):
        st.session_state.access_token = None
        st.session_state.username = None
        st.session_state.role = None
        st.rerun()

# Main app logic
if st.session_state.access_token:
    show_chatbot()
else:
    show_login()