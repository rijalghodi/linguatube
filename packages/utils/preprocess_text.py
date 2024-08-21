from langchain_core.documents import Document
from langchain.text_splitter import TokenTextSplitter

def split_text(text: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> list[str]:
    token_splitter = TokenTextSplitter(chunk_overlap=chunk_overlap, chunk_size=chunk_size)
    tokens = token_splitter.split_text(text)
    return tokens

def texts_to_docs(texts: list[str], metadata: dict[str, str]) -> list[Document]:
    return [Document(page_content=page_content, metadata=metadata) for page_content in texts]

