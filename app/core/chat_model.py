from langchain_core.language_models import BaseChatModel
from langchain_openai import ChatOpenAI


def get_chat_model(api_key: str) -> BaseChatModel:
    return ChatOpenAI(model="gpt-4o-mini", openai_api_key=api_key)