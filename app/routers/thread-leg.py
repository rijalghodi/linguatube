# import uuid
# from typing import Literal, Optional

# from fastapi import APIRouter, Depends
# from langchain_core.tools import create_retriever_tool
# from langgraph.checkpoint.postgres import PostgresSaver
# from langgraph.prebuilt import create_react_agent
# from psycopg_pool import ConnectionPool
# from pydantic import BaseModel
# from supabase import Client

# from app.core.chat_model import get_chat_model
# from app.core.connection_pool import get_connection_pool
# from app.core.db_client import get_client
# from app.core.vectorstore import get_vectorstore
# from app.service import insert_thread, list_thread


# class ThreadData(BaseModel):
#     pass

# class ThreadMetadata(BaseModel):
#     id: str
#     video_id: str
#     thread_id: str
#     title: str = None
#     mode: str = None

# class ThreadListData(BaseModel):
#     data: list[ThreadMetadata]
#     count: int

# class CreateThreadRequest(BaseModel):
#     title: Optional[str]
#     mode: Optional[Literal["chat", "practice"]] = "chat"
#     api_key: str

# class InsertThreadMessageRequest(BaseModel):
#     role: str
#     content: str
#     api_key: str

# class MessageData(BaseModel):
#     role: str
#     content: str
# class MessageListData(BaseModel):
#     data: list[MessageData]
#     count: int

# router = APIRouter()

# @router.post("/video/{video_id}/thread/")
# def create_thread(
#         request: CreateThreadRequest,
#         video_id: str,
#         client: Client = Depends(get_client),
#         pool: ConnectionPool = Depends(get_connection_pool)
# ):
#     vectorstore = get_vectorstore(request.api_key)
    
#     retriever_tool = create_retriever_tool(
#         vectorstore.as_retriever(search_type="similarity", filter={"video_id": video_id}),
#         name="retrieve_document",
#         description="Search and return information from content that may user ask.",
#     )

#     tools = [retriever_tool]

#     thread_id = str(uuid.uuid4())

#     if request.mode == "chat":
#         system_message = ("You are an assistant to help user learn english from youtube video.",
#                           "The youtube video content has been extracted and provided in tools.",
#                           "Feel free to use that to retrieve information related to videos."
#                           "Make answer very concise and keep conversation engaging. Maintain the user"
#                           "contribution in chat. "
#                           )
#     elif request.mode == "practice":
#         system_message = ("You are an assistant to help user learn english from youtube video.",
#                            "The youtube video content has been extracted and provided in tools.",
#                           "User chat will be recorded and assessed to track their english skills."
#                           "Make answer very concise and ask user with question related to the video."
#                           "Challenge user knowledge by asking information about video"
#                           )
#     else:
#         system_message = ("You are an assistant to help user learn english from youtube.",)

#     model = get_chat_model(request.api_key)

#     with pool.connection() as conn:
#         checkpointer = PostgresSaver(conn)
#         checkpointer.setup()  # Setup checkpointer if this is the first usage

#         graph = create_react_agent(model, tools=tools, checkpointer=checkpointer)
#         config = {"configurable": {"thread_id": thread_id}}
#         graph.invoke(
#             {"messages": [("system", "You will become an assistant to help user learn english from youtube. "
#                                      "First chat him How can I assist you today")]}, config)
#         # graph.invoke({"messages": [SystemMessage(content=system_message)]}, config)

#     new_thread = insert_thread(client, video_id, thread_id, title=request.title, mode=request.mode)

#     return new_thread


# @router.post("/video/{video_id}/thread/{thread_id}/")
# def insert_thread_message(
#         request: InsertThreadMessageRequest,
#         video_id: str,
#         thread_id: str,
#         pool: ConnectionPool = Depends(get_connection_pool),
# ):

#     vectorstore = get_vectorstore(request.api_key)

#     retriever_tool = create_retriever_tool(
#         vectorstore.as_retriever(search_type="similarity", filter={"video_id": video_id}),
#         name="retrieve_document",
#         description="Search and return information from youtube video that may user ask.",
#     )

#     tools = [retriever_tool]

#     model = get_chat_model(request.api_key)


#     with pool.connection() as conn:
#         checkpointer = PostgresSaver(conn)
#         checkpointer.setup()  # Setup checkpointer if this is the first usage
#         prompt = "Make your reply concise way in less than 250 word. Encourage user to more speak."

#         graph = create_react_agent(model, tools=tools, checkpointer=checkpointer, state_modifier=prompt)
#         config = {"configurable": {"thread_id": thread_id}}
#         result = graph.invoke({"messages": [(request.role, request.content)]}, config)

#     message = result['messages'][-1]

#     return {
#         "content": message.content,
#         "role": message.type,
#     }






# class GetAllMessageRequest(BaseModel):
#     api_key: str
# @router.get("/thread/{thread_id}/message", response_model=MessageListData)
# def get_all_message(
#         thread_id: str,
#         api_key: str,
#         # request: GetAllMessageRequest,
#         # model: BaseChatModel = Depends(get_chat_model),
#         pool: ConnectionPool = Depends(get_connection_pool),
# ):

#     vectorstore = get_vectorstore(api_key)
    
#     retriever_tool = create_retriever_tool(
#         vectorstore.as_retriever(),
#         name="retrieve_document",
#         description="Search and return information from content that may user ask.",
#     )

#     tools = [retriever_tool]

#     model = get_chat_model(api_key)

#     with pool.connection() as conn:
#         checkpointer = PostgresSaver(conn)
#         checkpointer.setup()  # Setup checkpointer if this is the first usage

#         graph = create_react_agent(model, tools=tools, checkpointer=checkpointer)
#         config = {"configurable": {"thread_id": thread_id}}
#         # print(config)
#         # print(graph.get_state(config))
#         # print(graph.get_state(config).values)
#         # print(graph.get_state(config).values['messages'])
#         # state = graph.get_state(config)
#         state = graph.get_state(config).values['messages']

#     messages = [ {"role": v.type, "content": v.content} for v in state ]
#     return {
#         "data": messages,
#         "count": len(messages)
#     }
#     # return {
#     #     "data": [],
#     #     "count": 0
#     # }
