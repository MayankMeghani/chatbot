from models import get_embedding_model
from vectorstore import get_vector_store

class department_classifier:
    
    def __init__(self):
        self.vector_store=get_vector_store(get_embedding_model(), collection_name="metadata", persist_directory="chroma_db")
    
    def retriver(self,query,top_k=1):
        """
        Retrieve documents based on the query and classify them into departments.
        """
        results = self.vector_store.similarity_search(query, k=top_k)
        top_department = results[0].metadata.get("department", "general")
        return top_department

if __name__ == "__main__":
    classifier = department_classifier()
    query = "How do we handle onboarding and exit processes?"
    top_department = classifier.retriver(query)
    print(f"The top department for the query '{query}' is: {top_department}")
