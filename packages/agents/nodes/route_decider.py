from langchain_core.language_models import BaseChatModel
from langchain_openai import ChatOpenAI
from langchain_core.tools import Tool
from packages.agents.shared.types import AgentState

class RouteDecider:

    def __init__(self, tools: list[Tool], chat_model: BaseChatModel):
        self.tools = tools
        self.chat_model = chat_model

    def __call__(self, *args, **kwargs):
        def decide_route(state: AgentState):
            """
            Invokes the agent model to generate a response based on the current state. Given
            the question, it will decide to retrieve using the retriever tool, or simply end.

            Args:
                state (messages): The current state

            Returns:
                dict: The updated state with the agent response appended to messages
            """
            print("---CALL AGENT---")
            messages = state["messages"]
            model = ChatOpenAI(temperature=0, streaming=True, model="gpt-4-turbo")
            model = model.bind_tools(self.tools)
            response = model.invoke(messages)
            # We return a list, because this will get added to the existing list
            return {"messages": [response]}
        return decide_route