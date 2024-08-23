from langchain_openai import OpenAIEmbeddings

def get_openai_embeddings(api_key: str):
    return OpenAIEmbeddings(openai_api_type=api_key)