from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableSequence
from rag.memorystore import MemoryStore
from rag.models import get_llm, get_pandas_agent
from rag.prompts import get_pandas_agent_prompt, get_format_prompt

class PandasPipeline:
    def __init__(self, dataframe=None, memory_store: MemoryStore = None, llm=None):
        self.llm = llm or get_llm()
        self.df = dataframe
        self.memory_store = memory_store or MemoryStore()
        self.parser = StrOutputParser()

        # Stage 1: Query Rewriter
        self.rewrite_prompt = get_pandas_agent_prompt()
        self.rewriter_chain = RunnableSequence(self.rewrite_prompt | self.llm | self.parser)

        # Stage 2: Pandas Agent (LangChain agent using df)
        self.pandas_agent = get_pandas_agent(dataframe=self.df, base_model=self.llm)

        # Stage 3: Output Formatter
        self.format_prompt = get_format_prompt()
        self.formatter_chain = RunnableSequence(self.format_prompt | self.llm | self.parser)

    def run(self, query: str, session_id: str) -> str:
        # Get session memory
        history = self.memory_store.get_history(session_id)
        history_text = get_buffer_string(history.messages)

        # Stage 1: Rewrite query using chat history
        rewritten_query = self.rewriter_chain.invoke({
            "question": query,
            "chat_history": history_text
        })

        # Stage 2: Query the dataframe
        try:
            agent_result = self.pandas_agent.invoke(rewritten_query)
        except Exception as e:
            agent_result = f"Agent failed: {e}"

        # Stage 3: Format final output
        final_response = self.formatter_chain.invoke({
            "query": query,
            "raw_output": agent_result
        })

        # Update memory
        history.add_user_message(query)
        history.add_ai_message(final_response)

        return final_response

def get_buffer_string(messages):
    """Convert ChatMessageHistory to plain text format."""
    buffer = ""
    for msg in messages:
        role = "User" if msg.type == "human" else "AI"
        buffer += f"{role}: {msg.content}\n"
    return buffer.strip()
