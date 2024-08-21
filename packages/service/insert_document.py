from supabase import Client

from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_core.documents import Document
from langchain_community.vectorstores import SupabaseVectorStore

from packages import split_text, texts_to_docs, random_bigint


def insert_document(
    client: Client,
    documents: list[Document],
) -> list[str]:
    embeddings = OpenAIEmbeddings()
    vector_store = SupabaseVectorStore(
        client=client,
        embedding=embeddings,
        table_name="documents",
        query_name="match_documents",
    )
    response = vector_store.add_documents(documents, ids=[random_bigint() for _ in range(len(documents))])

    return response
