from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain

from langchain_experimental.agents import create_pandas_dataframe_agent
import pandas as pd
from dotenv import load_dotenv
import os
load_dotenv()

if 'OPENAI_API_KEY' not in os.environ:
    raise ValueError("Missing API_KEY in environment variables")

def get_embedding_model(model_name="text-embedding-3-small"):
    return OpenAIEmbeddings(model=model_name)

def get_llm(model_name="gpt-4o",temperature=0.5):
    return ChatOpenAI(model=model_name, temperature=temperature)

def get_chat_model():
    llm = get_llm()
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    return ConversationChain(llm=llm, memory=memory, verbose=False)

def get_pandas_agent(base_model=None,dataframe=None):
    if dataframe is None:
        try:
            dataframe = pd.read_csv("../resources/data/hr/hr_data.csv")
        except FileNotFoundError:
            raise ValueError("No dataframe provided and default CSV not found")
    if dataframe.empty:
        raise ValueError("HR dataset is empty")
    return create_pandas_dataframe_agent(
        llm= base_model or get_llm(),
        df=dataframe,
        agent_type="openai-tools",
        **{"allow_dangerous_code": True} 
    )

