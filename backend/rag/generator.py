import logging
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableSequence
from rag.models import get_llm
from rag.prompts import get_default_prompt_template


class AnswerGenerator:
    def __init__(self, llm=None, prompt_template=None,parser=None):
        # Initialize logger
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)

        self.llm = llm or get_llm("gpt-4o", temperature=0.2)
        self.prompt_template = prompt_template or get_default_prompt_template()
        self.parser = parser or StrOutputParser()

        # Set up the invocation sequence
        self.generator_chain = RunnableSequence(self.prompt_template | self.llm | self.parser)

    def generate_answer(self, question: str, docs: list):
        """
        Generate an answer using the provided question and context from documents.
        
        Args:
            question (str): The question to answer.
            docs (list): List of documents providing context.

        Returns:
            str: Generated answer.
        """
        try:
            if not isinstance(docs, list):
                raise ValueError("Documents must be provided as a list.")
            
            context = "\n\n".join([
                f"Source: {doc.page_content}\n{doc.metadata['source']}\n" 
                for doc in docs if doc.page_content
            ])


            return self.generator_chain.invoke({"context": context, "question": question})
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