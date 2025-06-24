from typing import Dict
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from pydantic import BaseModel
from datetime import datetime, timedelta
from jose import JWTError, jwt

from rag.models import get_embedding_model, get_pandas_agent
from rag.vectorstore import get_vector_store
from rag.generator import AnswerGenerator
from rag.retriever import DocumentRetriever
from rag.pipelines import RAGPipeline

# ────────────────────────────────
# Auth + App Setup
# ────────────────────────────────

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = "secret-key"
ALGORITHM = "HS256"

users_db: Dict[str, Dict[str, str]] = {
    "Tony": {"password": "password123", "role": "engineering"},
    "Bruce": {"password": "securepass", "role": "marketing"},
    "Sam": {"password": "financepass", "role": "finance"},
    "Peter": {"password": "pete123", "role": "engineering"},
    "Sid": {"password": "sidpass123", "role": "marketing"},
    "Natasha": {"password": "hrpass123", "role": "hr"}
}

# ────────────────────────────────
# Request Models
# ────────────────────────────────

class ChatRequest(BaseModel):
    query: str

# ────────────────────────────────
# Utility Functions
# ────────────────────────────────

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=1)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return {"username": payload.get("sub"), "role": payload.get("role")}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

# ────────────────────────────────
# Startup Initialization
# ────────────────────────────────

@app.on_event("startup")
def initialize_pipeline():
    embedding_model = get_embedding_model()
    vector_store = get_vector_store(embedding_model)
    pandas_agent = get_pandas_agent()
    retriever = DocumentRetriever(vector_store)
    generator = AnswerGenerator()
    pipeline = RAGPipeline(retriever, generator, pandas_agent)

    # Attach to app state
    app.state.embedding = embedding_model
    app.state.vector_store = vector_store
    app.state.pandas_agent = pandas_agent
    app.state.retriever = retriever
    app.state.generator = generator
    app.state.pipeline = pipeline

# ────────────────────────────────
# Endpoints
# ────────────────────────────────

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = users_db.get(form_data.username)
    if not user or user["password"] != form_data.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": form_data.username, "role": user["role"]})
    return {"access_token": token, "token_type": "bearer"}

@app.post("/chatbot")
def chatbot(request: ChatRequest, current_user: Dict = Depends(get_current_user)):
    pipeline = app.state.pipeline
    session_id = current_user["username"]
    role = current_user["role"]

    result = pipeline.run(request.query, role, session_id)

    return {
        "message": result["result"],
        "mode": result["mode"],
        "status": result["status"]
    }

@app.post("/clear_memory")
def clear_memory(current_user: dict = Depends(get_current_user)):
    session_id = current_user["username"]
    generator: AnswerGenerator = app.state.generator
    generator.reset_memory(session_id)
    return {"message": "Memory cleared successfully."}
