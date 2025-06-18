from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
import os
os.environ["OPENAI_API_KEY"] = "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"


def get_embedding_model(model_name="text-embedding-3-small"):
    return OpenAIEmbeddings(model=model_name)

def get_llm(model_name="gpt-4o",temperature=0.2):
    return ChatOpenAI(model=model_name, temperature=temperature)