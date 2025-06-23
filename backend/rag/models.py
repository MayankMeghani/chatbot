from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain_experimental.agents import create_pandas_dataframe_agent
import pandas as pd
import os
os.environ["OPENAI_API_KEY"] = "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"

def get_embedding_model(model_name="text-embedding-3-small"):
    return OpenAIEmbeddings(model=model_name)

def get_llm(model_name="gpt-4o",temperature=0.2):
    return ChatOpenAI(model=model_name, temperature=temperature)

def get_pandas_agent():
    dataframe = pd.read_csv("../resources/data/hr/hr_data.csv")
    if dataframe.empty:
        raise ValueError("HR dataset is empty")
    return create_pandas_dataframe_agent(
        llm=get_llm(),
        df=dataframe,
        # suffix ="list as table",
        # verbose=True,
        # include_df_in_prompt=False,  # Explicitly set to False
        **{"allow_dangerous_code": True} 
    )

