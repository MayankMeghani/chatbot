from langchain_chroma import Chroma
# from models import get_embedding_model
def get_vector_store(embedding_model, collection_name="documents", persist_directory="chroma_db"):
    return Chroma(
        collection_name=collection_name,
        embedding_function=embedding_model,
        persist_directory=persist_directory
    )

# if __name__ == "__main__":
#     vector_store = get_vector_store(get_embedding_model())

#     # List of IDs to delete (exactly the 5 you provided)
#     ids_to_delete = [
#         "d04002e4-1329-4484-a106-92853f65a39e",
#         "aa01ea07-6e1d-4bf8-81a6-a8751c84a3b1",
#         "da747ee6-c07e-423f-96a3-c9716f8a4c2f",
#         "fb44bed9-d7c2-47d5-9022-1e77bfcc2b09",
#         "2250ed7e-6f59-488e-808b-c1110dcb91f9"
#     ]

#     # Verify if these IDs exist before deleting
#     existing_ids = vector_store.get()["ids"]
#     found_ids = [doc_id for doc_id in ids_to_delete if doc_id in existing_ids]

#     if found_ids:
#         vector_store.delete(found_ids)
#         print(f"✅ Deleted {len(found_ids)} documents.")
#     else:
#         print("ℹ️ None of the specified documents were found.")