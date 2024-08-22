from langchain_core.language_models import BaseChatModel
from langchain_openai import ChatOpenAI

def get_chat_model() -> BaseChatModel:
    return ChatOpenAI(model="gpt-4o-mini")