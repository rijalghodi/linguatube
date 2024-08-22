from langchain_core.output_parsers import StrOutputParser
from packages.prompts import word_info_prompt, translation_prompt

from pydantic import BaseModel
from fastapi import APIRouter, Depends

from langchain_openai import ChatOpenAI

class TranslateOutputData(BaseModel):
    output: str

class TranslateRequest(BaseModel):
    word: str
    sentence: str
    language: str
    api_key: str

class WordInfoOutputData(BaseModel):
    output: str

class WordInfoRequest(BaseModel):
    word: str
    sentence: str
    api_key: str

router = APIRouter()

@router.post("/translate/")
def translate_word(request: TranslateRequest):
    model = ChatOpenAI(model="gpt-4o-mini", api_key=request.api_key)
    chain = translation_prompt | model | StrOutputParser()
    res = chain.invoke({"language": request.language, "word": request.word, "sentence": request.sentence})
    return {"output": res}

@router.post("/word-info/")
def word_info(request: WordInfoRequest):
    model = ChatOpenAI(model="gpt-4o-mini", api_key=request.api_key)
    chain = word_info_prompt | model | StrOutputParser()
    res = chain.invoke({ "word": request.word, "sentence": request.sentence})
    return {"output": res}


