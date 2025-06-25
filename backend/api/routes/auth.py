from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from core.auth import create_access_token
from services.dummy_db import add_user, verify_user

router = APIRouter()

ROLE_ACCESS = {
    "finance", "marketing", "hr", "engineering", "C-Level", "employee"
}

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = verify_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": form_data.username, "role": user["role"]})
    return {"access_token": token, "token_type": "bearer"}

class SignupRequest(BaseModel):
    username: str
    password: str
    role: str

@router.post("/signup")
def signup(request: SignupRequest):
    if request.role not in ROLE_ACCESS:
        raise HTTPException(status_code=400, detail="Invalid role")

    if not add_user(request.username, request.password, request.role):
        raise HTTPException(status_code=409, detail="User already exists")

    return {"message": "User registered successfully"}
