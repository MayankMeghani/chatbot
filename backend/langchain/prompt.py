from langchain.prompts import PromptTemplate

def get_default_prompt_template():
    """
    Returns a default prompt template for answering questions based on context.
    """
    return PromptTemplate(
            input_variables=["context", "question"],
            template=(
                "You are a helpful assistant. Use the following context to answer the question.\n\n"
                "Context:\n{context}\n\n"
                "Question:\n{question}\n\n"
                "Answer in a clear and concise manner."
            )
        )