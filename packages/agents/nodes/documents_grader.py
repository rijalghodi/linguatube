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


class DocumentRelevanceGrader:

    def __init__(self, chat_model: BaseChatModel):
        self.chat_model = chat_model

    def __call__(self, *args, **kwargs):

        def grade_documents(state) -> Literal["generate", "rewrite"]:
            """
            Determines whether the retrieved documents are relevant to the question.

            Args:
                state (messages): The current state

            Returns:
                str: A decision for whether the documents are relevant or not
            """

            print("---CHECK RELEVANCE---")

            # Data model
            class grade(BaseModel):
                """Binary score for relevance check."""

                binary_score: str = Field(description="Relevance score 'yes' or 'no'")

            # LLM with tool and validation
            llm_with_tool = self.chat_model.with_structured_output(grade)

            # Prompt
            prompt = PromptTemplate(
                template="""You are a grader assessing relevance of a retrieved document to a user question. \n 
                Here is the retrieved document: \n\n {context} \n\n
                Here is the user question: {question} \n
                If the document contains keyword(s) or semantic meaning related to the user question, grade it as relevant. \n
                Give a binary score 'yes' or 'no' score to indicate whether the document is relevant to the question.""",
                input_variables=["context", "question"],
            )

            # Chain
            chain = prompt | llm_with_tool

            messages = state["messages"]
            last_message = messages[-1]

            question = messages[0].content
            docs = last_message.content

            scored_result = chain.invoke({"question": question, "context": docs})

            score = scored_result.binary_score

            if score == "yes":
                print("---DECISION: DOCS RELEVANT---")
                return "generate"

            else:
                print("---DECISION: DOCS NOT RELEVANT---")
                print(score)
                return "rewrite"

        return grade_documents

