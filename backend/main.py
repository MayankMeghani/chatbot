from rag.retriever import DocumentRetriever
from rag.generator import AnswerGenerator
from rag.models import get_embedding_model,get_pandas_agent
from rag.vectorstore import get_vector_store
from rag.pipelines import RAGPipeline
from typing import Dict

from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from fastapi import status

from datetime import datetime, timedelta
from jose import JWTError,jwt

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
SECRET_KEY = "secret-key"  # Replace with environment variable in production
ALGORITHM = "HS256"

# Dummy user database
users_db: Dict[str, Dict[str, str]] = {
    "Tony": {"password": "password123", "role": "engineering"},
    "Bruce": {"password": "securepass", "role": "marketing"},
    "Sam": {"password": "financepass", "role": "finance"},
    "Peter": {"password": "pete123", "role": "engineering"},
    "Sid": {"password": "sidpass123", "role": "marketing"},
    "Natasha": {"passwoed": "hrpass123", "role": "hr"}
}




def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=1)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Login endpoint
@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = users_db.get(form_data.username)
    if not user or user["password"] != form_data.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": form_data.username, "role": user["role"]})
    return {"access_token": token, "token_type": "bearer"}


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return {"username": payload.get("sub"), "role": payload.get("role")}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

# Example protected endpoint: Only accessible to engineering and c_level
@app.get("/chatbot")
def chatbot(current_user: Dict = Depends(get_current_user)):
    embedding = get_embedding_model()
    vector_store = get_vector_store(embedding)
    pandas_agent = get_pandas_agent() 
    retriever = DocumentRetriever(vector_store)
    generator = AnswerGenerator()
    pipeline = RAGPipeline(retriever, generator, pandas_agent)