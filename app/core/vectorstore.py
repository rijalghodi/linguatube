from fastapi import Depends
from langchain_community.vectorstores import SupabaseVectorStore
from langchain_openai import OpenAIEmbeddings
from supabase import Client

from app.core.db_client import get_client
from app.core.embedding import get_openai_embeddings


def get_vectorstore(
        api_key: str,
        client: Client = Depends(get_client),
) -> SupabaseVectorStore:
    
    vectorstore = SupabaseVectorStore(
        client=client,
        embedding=OpenAIEmbeddings(openai_api_key=api_key),
        table_name="documents",
        query_name="match_documents",
    )
    # vectorstore.similarity_search()
    return vectorstore
