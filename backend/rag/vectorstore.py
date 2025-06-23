from langchain_chroma import Chroma
from rag.models import get_embedding_model

def get_vector_store(embedding_model, collection_name="documents", persist_directory="chroma_db"):
    return Chroma(
        collection_name=collection_name,
        embedding_function=embedding_model,
        persist_directory=persist_directory
    )

if __name__ == "__main__":
    vector_store = get_vector_store(get_embedding_model())

    all_docs = vector_store.get()["documents"]
    all_metadatas = vector_store.get()["metadatas"]
    all_ids = vector_store.get()["ids"]

    hr_ids = [
        _id for _id, metadata in zip(all_ids, all_metadatas)
        if metadata.get("department", "").lower() == "hr"
    ]

    if hr_ids:
        vector_store.delete(hr_ids)
        print(f"✅ Deleted {len(hr_ids)} documents from HR department.")
    else:
        print("ℹ️ No HR documents found to delete.")
