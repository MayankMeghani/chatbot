class RAGPipeline:
    def __init__(self, retriever, generator, pandas_agent):
        self.retriever = retriever
        self.generator = generator
        self.pandas_agent = pandas_agent

    def run(self, query: str, user_role: str):
        route = self.retriever.decide_execution_path(query, user_role)

        if route == "pandas":
            agent_output = self.pandas_agent.invoke(query)
            return {
                "mode": "pandas",
                "status": "ok",
                "result": agent_output["output"]
            }

        elif route == "rag":
            retrieval_result = self.retriever.retrieve(query, user_role)

            if retrieval_result["status"] == "ok":
                docs = self.retriever.format_results(retrieval_result["docs"])
                answer = self.generator.generate_answer(query, docs)
                return {
                    "mode": "rag",
                    "status": "ok",
                    "retrieved_docs": len(docs),
                    "result": answer
                }

            return {
                "mode": "rag",
                "status": retrieval_result["status"],
                "result": retrieval_result["message"]
            }

        else:
            return {
                "mode": "unknown",
                "status": "error",
                "result": "Unexpected routing decision."
            }
