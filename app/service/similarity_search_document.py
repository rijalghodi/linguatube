from langchain_community.vectorstores import SupabaseVectorStore
from langchain_core.documents import Document


def similarity_search_document(
    vector_store: SupabaseVectorStore,
    video_id: str,
        query: str,
        k: int = None,
) -> list[Document]:
    response = vector_store.similarity_search(query, k, {
        video_id: video_id,
    })

    return response