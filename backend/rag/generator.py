import logging
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableSequence
from rag.models import get_llm
from rag.prompts import get_default_prompt_template
from langchain_core.runnables import RunnableWithMessageHistory

class AnswerGenerator:
    def __init__(self,memory_store, llm=None, prompt_template=None, parser=None):
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)
        self.memory_registry = {}
        self.llm = llm or get_llm()
        self.prompt_template = prompt_template or get_default_prompt_template()
        self.parser = parser or StrOutputParser()
        self.memory_store = memory_store

        # Base chain
        self.base_chain = RunnableSequence(self.prompt_template | self.llm | self.parser)

        # Memory-aware chain
        self.chain_with_memory = RunnableWithMessageHistory(
            self.base_chain,
            lambda session_id: self.memory_store.get_history(session_id),
            input_messages_key="question",
            history_messages_key="history"
        )
        
        
    def generate_answer(self, question: str, docs: list, session_id: str):
        try:
            if not isinstance(docs, list):
                raise ValueError("Documents must be provided as a list.")

            context = "\n\n".join([
                f"Source: {doc.page_content}\n{doc.metadata['source']}"
                for doc in docs
                if doc.page_content and "source" in doc.metadata
            ])


            # Must match prompt template keys
            inputs = {
                "context": context,
                "question": question
            }

            return self.chain_with_memory.invoke(
                inputs,
                config={"configurable": {"session_id": session_id} }  
            )

        except Exception as e:
            self.logger.error(f"Error generating answer: {e}")
            return None

# Example Usage
if __name__ == "__main__":
    generator = AnswerGenerator()
    question = "What are the company's leave policies?"
    docs = []  # Assume this is a list of Document objects
    answer = generator.generate_answer(question, docs)
    print(answer)