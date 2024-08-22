from langchain_community.vectorstores import SupabaseVectorStore
from langchain_openai import OpenAIEmbeddings
from supabase import Client
from fastapi import Depends
from app.core.embedding import get_openai_embeddings
from app.core.db_client import get_client

def get_vectorstore(
        client: Client = Depends(get_client),
        embeddings: OpenAIEmbeddings = Depends(get_openai_embeddings)):
    vectorstore = SupabaseVectorStore(
        client=client,
        embedding=embeddings,
        table_name="documents",
        query_name="match_documents",
    )
    # vectorstore.similarity_search()
    return vectorstore
