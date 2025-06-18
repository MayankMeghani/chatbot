from langchain_chroma import Chroma

def get_vector_store(embedding_model, collection_name="documents", persist_directory="chroma_db"):
    return Chroma(
        collection_name=collection_name,
        embedding_function=embedding_model,
        persist_directory=persist_directory
    )
