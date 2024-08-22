from langchain_core.vectorstores import VectorStore
from langchain.tools.retriever import create_retriever_tool

def create_vector_store_retriever(vectorstore: VectorStore) -> Tool:

    retriever = vectorstore.as_retriever()

    retriever_tool = create_retriever_tool(
        retriever,
        name="retrieve_document",
        description="Search and return information from content that may user ask.",
    )

    return retriever_tool
