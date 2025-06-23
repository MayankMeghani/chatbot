from retriever import DocumentRetriever
from generator import AnswerGenerator
from models import get_embedding_model,get_pandas_agent
from vectorstore import get_vector_store
from pipelines import RAGPipeline
def main():
    embedding = get_embedding_model()
    vector_store = get_vector_store(embedding)
    pandas_agent = get_pandas_agent() 
    retriever = DocumentRetriever(vector_store)
    generator = AnswerGenerator()
    pipeline = RAGPipeline(retriever, generator, pandas_agent)

    query = "list all employees with their leave balances desending on their department"
    user_role = "hr"

    result = pipeline.run(query, user_role)

    print(f"\n🧭 Mode: {result['mode'].upper()}")
    print(f"✅ Status: {result['status'].upper()}")
    if result["status"] == "ok":
        if result["mode"] == "rag":
            print(f"📄 Docs Used: {result['retrieved_docs']}")
            print(f"\n💬 Answer:\n{result['result']}")
        else:
            print(f"\n🚫 Message: {result['result']}")                                        


if __name__ == "__main__":
    main()
