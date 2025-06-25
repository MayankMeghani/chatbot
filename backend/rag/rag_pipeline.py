class RAGPipeline:
    def __init__(self, retriever, generator):
        self.retriever = retriever
        self.generator = generator

    def run(self, query: str, user_role: str, session_id: str) -> dict:
        try:
            # Step 1: Retrieve relevant documents
            retrieval_result = self.retriever.retrieve(query, user_role)

            if retrieval_result["status"] != "ok":
                return {
                    "mode": "rag",
                    "status": retrieval_result["status"],
                    "result": retrieval_result["message"]
                }

            # Step 2: Format documents
            docs = self.retriever.format_results(retrieval_result["docs"])

            # Step 3: Generate final answer
            answer = self.generator.generate_answer(query, docs, session_id)

            return {
                "mode": "rag",
                "status": "ok",
                "retrieved_docs": len(docs),
                "result": answer
            }

        except Exception as e:
            return {
                "mode": "rag",
                "status": "error",
                "result": f"Unhandled RAG pipeline error: {str(e)}"
            }
