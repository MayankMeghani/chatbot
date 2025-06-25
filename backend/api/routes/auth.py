from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from core.auth import create_access_token, users_db

router = APIRouter()

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = users_db.get(form_data.username)
    if not user or user["password"] != form_data.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": form_data.username, "role": user["role"]})
    return {"access_token": token, "token_type": "bearer"}


class SignupRequest(BaseModel):
    username: str
    password: str
    role: str  # department

@router.post("/signup")
def signup(request: SignupRequest):
    if request.username in users_db:
        raise HTTPException(status_code=409, detail="User already exists")
    
    if request.role not in ["finance", "marketing", "hr", "engineering", "C-Level", "employee"]:
        raise HTTPException(status_code=400, detail="Invalid role")
    
    users_db[request.username] = {
        "password": request.password,
        "role": request.role
    }
    return {"message": "User registered successfully"}
