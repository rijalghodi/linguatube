from pydantic import BaseModel


class WordInfoOutputData(BaseModel):
    output: str

class WordInfoRequest(BaseModel):
    word: str
    sentence: str
    api_key: str

class TranslateOutputData(BaseModel):
    output: str

class TranslateRequest(BaseModel):
    word: str
    sentence: str
    language: str
    api_key: str