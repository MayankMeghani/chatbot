import json
from pathlib import Path

USER_FILE = Path("users.json")

def load_users():
    if USER_FILE.exists():
        with open(USER_FILE, "r") as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f, indent=2)

def get_user(username):
    users = load_users()
    return users.get(username)

def add_user(username, password, role):
    users = load_users()
    if username in users:
        return False  # User already exists
    users[username] = {"password": password, "role": role}
    save_users(users)
    return True

def verify_user(username, password):
    user = get_user(username)
    return user if user and user["password"] == password else None
