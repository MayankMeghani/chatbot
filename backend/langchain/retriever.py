class DocumentRetriever:
    def __init__(self, vector_store, top_k=3):
        self.vector_store = vector_store
        self.top_k = top_k

    def retrieve(self, query: str):
        try:
            results = self.vector_store.similarity_search_with_score(query, k=self.top_k)
            return results
        except Exception as e:
            print("Retrieval error: {e}")
            return []

    def format_results(self, results):
        return [
            {
                "content": doc.page_content,
                "metadata": doc.metadata,
                "score": score
            }
            for doc, score in results
        ]
