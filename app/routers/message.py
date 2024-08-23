from fastapi import APIRouter, Depends, HTTPException
from langchain_core.tools import create_retriever_tool
from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.prebuilt import create_react_agent
from psycopg_pool import ConnectionPool
from supabase import Client

from app.core.chat_model import get_chat_model
from app.core.connection_pool import get_connection_pool
from app.core.db_client import get_client
from app.core.vectorstore import get_vectorstore
from app.models import InsertMessageRequest, MessageListData

router = APIRouter()

@router.post("/video/{video_id}/thread/{thread_id}/")
async def insert_message(  
        request: InsertMessageRequest,
        video_id: str,
        thread_id: str,
        pool: ConnectionPool = Depends(get_connection_pool),
        client: Client = Depends(get_client),
):
    vectorstore = get_vectorstore(request.api_key, client)

    retriever_tool = create_retriever_tool(
        vectorstore.as_retriever(search_type="similarity", filter={"video_id": video_id}),
        name="retrieve_document",
        description="Search and return information from youtube video that may user ask.",
    )

    tools = [retriever_tool]
    model = get_chat_model(request.api_key)

    with pool.connection() as conn:
        checkpointer = PostgresSaver(conn)
        checkpointer.setup()
        prompt = "Make your reply concise way in less than 250 word. Encourage user to more speak."

        graph = create_react_agent(model, tools=tools, checkpointer=checkpointer, state_modifier=prompt)
        config = {"configurable": {"thread_id": thread_id}}
        try:
            result = graph.invoke({"messages": [(request.role, request.content)]}, config)
        except Exception as e:
            raise HTTPException(status_code=500, detail="Problem in generating message. " + str(e))

    message = result['messages'][-1]

    return {
        "content": message.content,
        "role": message.type,
    }

@router.get("/thread/{thread_id}/message", response_model=MessageListData)
async def get_all_message(
        thread_id: str,
        api_key: str,
        pool: ConnectionPool = Depends(get_connection_pool),
        client: Client = Depends(get_client),
):
    vectorstore = get_vectorstore(api_key, client)
    
    retriever_tool = create_retriever_tool(
        vectorstore.as_retriever(),
        name="retrieve_document",
        description="Search and return information from youtube content that may user ask.",
    )

    tools = [retriever_tool]
    model = get_chat_model(api_key)

    with pool.connection() as conn:
        checkpointer = PostgresSaver(conn)
        checkpointer.setup()

        graph = create_react_agent(model, tools=tools, checkpointer=checkpointer)
        config = {"configurable": {"thread_id": thread_id}}
        try:
            state = graph.get_state(config).values['messages']
        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail="Problem in get all message. " + str(e))

    messages = [{"role": v.type, "content": v.content} for v in state]
    return {
        "data": messages,
        "count": len(messages)
    }
