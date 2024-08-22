from langchain_core.language_models import BaseChatModel
from langchain_core.tools import create_retriever_tool
from langchain_core.vectorstores import VectorStore
from langgraph.checkpoint.base import Checkpoint

from packages.agents.nodes.route_decider import RouteDecider
from packages.agents.nodes.message_generator import MessageGenerator
from packages.agents.nodes.question_rewriter import QuestionRewriter
from packages.agents.nodes.documents_grader import DocumentRelevanceGrader

from langgraph.prebuilt import tools_condition

from langgraph.graph import END, StateGraph, START
from langgraph.prebuilt import ToolNode
from .shared.types import AgentState

class RAGChatAgent:
    def __init__(self, model: BaseChatModel, vectorstore: VectorStore, memory: Checkpoint):
        self.model = model
        self.vectorstore = vectorstore
        self.memory = memory

    def __call__(self, *args, **kwargs):
        # ---- Define Tools ----

        retriever_tool = create_retriever_tool(
            self.vectorstore.as_retriever(),
            name="retrieve_document",
            description="Search and return information from content that may user ask.",
        )

        tools = [retriever_tool]

        # ---- Define Nodes ----
        decide_route = RouteDecider(tools, self.model)
        generate_message = MessageGenerator(self.model)
        grade_documents = DocumentRelevanceGrader(self.model)
        rewrite_question = QuestionRewriter(self.model)

        # ---- Define Graph ----

        # Define a new graph
        workflow = StateGraph(AgentState)

        # Define the nodes we will cycle between
        workflow.add_node("decide", decide_route)  # decide using tools or end
        retrieve = ToolNode(tools)
        workflow.add_node("retrieve", retrieve)  # retrieve document
        workflow.add_node("rewrite", rewrite_question)  # Re-writing the question
        workflow.add_node(
            "generate", generate_message
        )  # Generating a response after we know the documents are relevant

        # Call agent node to decide to retrieve or not
        workflow.add_edge(START, "decide")

        # Decide whether to retrieve
        workflow.add_conditional_edges(
            "decide",
            # Assess agent decision
            tools_condition,
            {
                # Translate the condition outputs to nodes in our graph
                "tools": "retrieve",
                END: END,
            },
        )

        # Edges taken after the `action` node is called.
        workflow.add_conditional_edges(
            "retrieve",
            # Assess agent decision
            grade_documents,
        )
        workflow.add_edge("generate", END)
        workflow.add_edge("rewrite", "agent")

        graph = workflow.compile(self.memory)

