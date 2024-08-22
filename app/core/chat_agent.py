from contextlib import asynccontextmanager, contextmanager
from langchain_core.vectorstores import VectorStore
from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.prebuilt import create_react_agent
from packages.service.insert_thread import insert_thread
from psycopg_pool import ConnectionPool
from langchain_core.language_models import BaseChatModel
from langchain_core.tools import create_retriever_tool

@asynccontextmanager
async def chat_agent_context(
    pool: ConnectionPool,
    model: BaseChatModel,
    vectorstore: VectorStore,
):
    # Open a connection from the pool
    with pool.connection() as conn:
        try:
            retriever_tool = create_retriever_tool(
                vectorstore.as_retriever(),
                name="retrieve_document",
                description="Search and return information from content that may user ask.",
            )

            tools = [retriever_tool]
            # Setup the checkpointer
            checkpointer = PostgresSaver(conn)
            checkpointer.setup()  # Setup checkpointer if this is the first usage

            # Create the graph using the model, tools, and checkpointer
            graph = create_react_agent(model, tools=tools, checkpointer=checkpointer)

            # Yield the graph for use within the context
            yield graph

        finally:
            # Clean up the graph if necessary
            # (This is where you'd add any teardown code for the graph, if applicable)
            pass  # Replace with actual cleanup if needed