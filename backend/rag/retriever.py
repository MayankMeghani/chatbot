from rag.prompts import get_routing_prompt
from rag.models  import get_llm
from langchain_core.output_parsers import StrOutputParser

ROLE_ACCESS = {
    "finance": ["finance", "general"],
    "marketing": ["marketing", "general"],
    "hr": ["hr", "general"],
    "engineering": ["engineering", "general"],
    "C-Level": ["finance", "marketing", "hr", "engineering", "general"],
    "employee": ["general"]
}

class DocumentRetriever:
    def __init__(self, vector_store, top_k=5):
        self.vector_store = vector_store
        self.top_k = top_k
        self.routing_prompt = get_routing_prompt()
        self.llm = get_llm()

    def decide_execution_path(self, query: str, user_role: str) -> str:
        if user_role in ["hr", "C-Level"]:
            route_chain = self.routing_prompt | self.llm | StrOutputParser()
            route_result = route_chain.invoke({"input": query})
            return route_result
        return "rag"
    
    def retrieve(self, query: str, user_role: str):
        try:
            all_results = self.vector_store.similarity_search_with_score(query, k=self.top_k)
            print(all_results[0])
            if not all_results:
                return {
                    "status": "no_match",
                    "docs": [],
                    "message": "No relevant documents found for your query."
                }

            allowed_depts = ROLE_ACCESS.get(user_role, ["general"])
            filtered = [
                (doc, score)
                for doc, score in all_results
                if doc.metadata.get("department", "").lower() in [dept.lower() for dept in allowed_depts]
                ]

            if not filtered:
                return {
                    "status": "restricted",
                    "docs": [],
                    "message": "You do not have permission to access documents related to this query."
                }

            return {
                "status": "ok",
                "docs": filtered,
                "message": None
            }

        except Exception as e:
            print(f"Retrieval error: {e}")
            return {
                "status": "error",
                "docs": [],
                "message": f"Retrieval error occurred: {str(e)}"
            }
        
    def format_results(self, results):
        return [doc for doc, score in results]


