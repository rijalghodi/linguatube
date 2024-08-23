from langchain_community.vectorstores import SupabaseVectorStore
from langchain_core.documents import Document
from langchain_openai.embeddings import OpenAIEmbeddings
from supabase import Client

from app.core.vectorstore import get_vectorstore
from app.utils import random_bigint


def insert_document(
    client: Client,
    documents: list[Document],
    api_key: str,
) -> list[str]:
    vector_store = get_vectorstore(api_key, client)
    response = vector_store.add_documents(documents, ids=[random_bigint() for _ in range(len(documents))])

    return response
