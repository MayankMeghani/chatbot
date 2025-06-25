from api.routes import auth_router, chatbot_router

from rag.models import get_embedding_model
from rag.vectorstore import get_vector_store
from rag.generator import AnswerGenerator
from rag.retriever import DocumentRetriever
from rag.memorystore import MemoryStore

from rag.pandas_pipeline import PandasPipeline
import pandas as pd
from rag.rag_pipeline import RAGPipeline
from rag.router_pipeline import RouterPipeline
from  core.app import app

app.include_router(auth_router)
app.include_router(chatbot_router)

@app.on_event("startup")
def initialize_pipeline():
    embedding_model = get_embedding_model()
    vector_store = get_vector_store(embedding_model)
    memory_store = MemoryStore()
    retriever = DocumentRetriever(vector_store)
    generator = AnswerGenerator(memory_store)
    rag_pipeline = RAGPipeline(retriever, generator)
    pandas_pipeline = PandasPipeline()
    router_pipeline = RouterPipeline(rag_pipeline, pandas_pipeline)

    # app.state.embedding = embedding_model
    # app.state.vector_store = vector_store
    app.state.memory_store = memory_store
    # app.state.retriever = retriever
    # app.state.generator = generator
    app.state.router_pipeline = router_pipeline
    print("RAG pipeline initialized successfully.")
