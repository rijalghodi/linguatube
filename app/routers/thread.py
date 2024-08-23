import uuid

from fastapi import APIRouter, Depends, HTTPException
from langchain_core.messages import SystemMessage
from langchain_core.tools import create_retriever_tool
from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.prebuilt import create_react_agent
from psycopg_pool import ConnectionPool
from supabase import Client

from app.core.chat_model import get_chat_model
from app.core.connection_pool import get_connection_pool
from app.core.db_client import get_client
from app.core.vectorstore import get_vectorstore
from app.models import CreateThreadRequest, ThreadListData, ThreadMetaData
from app.service import list_thread
from app.service.insert_thread import insert_thread

router = APIRouter()

@router.post("/video/{video_id}/thread/", response_model=ThreadMetaData)
async def create_thread(
        request: CreateThreadRequest,
        video_id: str,
        client: Client = Depends(get_client),
        pool: ConnectionPool = Depends(get_connection_pool)
):
    vectorstore = get_vectorstore(request.api_key, client)
    
    retriever_tool = create_retriever_tool(
        vectorstore.as_retriever(search_type="similarity", filter={"video_id": video_id}),
        name="retrieve_document",
        description="Search and return information from youtube content that may user ask.",
    )

    tools = [retriever_tool]
    thread_id = str(uuid.uuid4())

    system_message = {
        "chat": "You are an assistant designed to help users learn English from YouTube videos. \
            The video content has been extracted and is available through tools for you to access. \
            Use these tools to retrieve information or summarize the video content. \
            Keep your responses concise, engaging, and ensure the user remains active in the conversation.",
        "practice": "You are an assistant designed to help users learn English using YouTube videos. \
            The content from these videos has been extracted and is available through tools. \
            User chats will be recorded and assessed to monitor their English skills. \
            Keep your responses concise, ask questions related to the video, and challenge the user’s understanding \
            by inquiring about specific details from the video."
    }.get(request.mode, ("You are an assistant to help user learn english from youtube.",))

    model = get_chat_model(request.api_key)

    with pool.connection() as conn:
        checkpointer = PostgresSaver(conn)
        checkpointer.setup()

        graph = create_react_agent(model, tools=tools, checkpointer=checkpointer)
        config = {"configurable": {"thread_id": thread_id}}
    
        try:
            graph.invoke(
                input={"messages": [SystemMessage(content=str(system_message))]}, config=config)
        except Exception as e:
            raise HTTPException(status_code=500, detail="Problem in creating thread. " + str(e))
    
    try:
        new_thread = insert_thread(client, video_id, thread_id, title=request.title, mode=request.mode)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Problem in inserting thread" + str(e))

    return new_thread

@router.get("/video/{video_id}/thread/", response_model=ThreadListData)
async def get_all_thread(video_id: str, client: Client = Depends(get_client)):
    try:
        threads = list_thread(client, video_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Problem in getting threads" + str(e))
    return threads