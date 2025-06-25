class RouterPipeline:
    def __init__(self, rag_pipeline, pandas_pipeline):
        self.rag_pipeline = rag_pipeline
        self.pandas_pipeline = pandas_pipeline

    def run(self, query: str, user_role: str, session_id: str) -> dict:
        """
        Decides which pipeline to use based on query type and routes accordingly.
        """

        # Rely on the retriever's routing logic
        route = self.rag_pipeline.retriever.decide_execution_path(query, user_role)

        if route == "pandas":
            result = self.pandas_pipeline.run(query, session_id)
            return {
                "mode": "pandas",
                "status": "ok",
                "result": result
            }

        elif route == "rag":
            return self.rag_pipeline.run(query, user_role, session_id)

        else:
            return {
                "mode": "unknown",
                "status": "error",
                "result": "Unexpected routing decision."
            }
