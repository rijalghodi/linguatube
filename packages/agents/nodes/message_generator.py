from langchain_core.tools import create_retriever_tool
from langchain_core.vectorstores import VectorStore
from typing import Annotated, Sequence, TypedDict

from langchain_core.messages import BaseMessage

from langgraph.graph.message import add_messages


class AgentState(TypedDict):
    # The add_messages function defines how an update should be processed
    # Default is to replace. add_messages says "append"
    messages: Annotated[Sequence[BaseMessage], add_messages]


from typing import Annotated, Literal, Sequence, TypedDict

from langchain import hub
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI

from langchain_core.language_models import BaseChatModel
from langchain_openai import ChatOpenAI
from langchain_core.tools import Tool
from packages.agents.shared.types import AgentState


class MessageGenerator:

    def __init__(self, chat_model: BaseChatModel):
        self.chat_model = chat_model

    def __call__(self, *args, **kwargs):
        def generate_message(state: AgentState):
            """
            Generate answer

            Args:
                state (messages): The current state

            Returns:
                 dict: The updated state with re-phrased question
            """
            print("---GENERATE---")
            messages = state["messages"]
            question = messages[0].content
            last_message = messages[-1]

            question = messages[0].content
            docs = last_message.content

            # Prompt
            prompt = hub.pull("rlm/rag-prompt")

            # Post-processing
            def format_docs(docs):
                return "\n\n".join(doc.page_content for doc in docs)

            # Chain
            rag_chain = prompt | self.chat_model | StrOutputParser()

            # Run
            response = rag_chain.invoke({"context": format_docs(docs), "question": question})
            return {"messages": [response]}

        return generate_message
