from retriever import DocumentRetriever
from generator import AnswerGenerator
from models import get_embedding_model
from vectorstore import get_vector_store

def main():
    embedding = get_embedding_model()
    vector_store = get_vector_store(embedding)

    retriever = DocumentRetriever(vector_store)
    generator = AnswerGenerator()

    query = "What is the leave policy for new employees?"
    results = retriever.retrieve(query)
    docs = [doc for doc, score in results]
    answer = generator.generate_answer(query, docs)
    print(f"\n💬 Answer:\n{answer}")

if __name__ == "__main__":
    main()
