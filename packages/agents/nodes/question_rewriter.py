from langchain_core.language_models import BaseChatModel
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


class QuestionRewriter:

    def __init__(self, chat_model: BaseChatModel):
        self.chat_model = chat_model

    def __call__(self, *args, **kwargs):
        def rewrite_question(state: AgentState):
            """
            Transform the query to produce a better question.

            Args:
                state (messages): The current state

            Returns:
                dict: The updated state with re-phrased question
            """

            print("---TRANSFORM QUERY---")
            messages = state["messages"]
            question = messages[0].content

            msg = [
                HumanMessage(
                    content=f""" \n 
            Look at the input and try to reason about the underlying semantic intent / meaning. \n 
            Here is the initial question:
            \n ------- \n
            {question} 
            \n ------- \n
            Formulate an improved question: """,
                )
            ]

            # Grader
            response = self.chat_model.invoke(msg)
            return {"messages": [response]}

        return rewrite_question
