from fastapi import APIRouter, HTTPException
from langchain_core.output_parsers import StrOutputParser

from app.core.chat_model import get_chat_model
from app.models import (TranslateOutputData, TranslateRequest,
                        WordInfoOutputData, WordInfoRequest)
from app.utils.prompts import translation_prompt, word_info_prompt

router = APIRouter()


@router.post("/word/translate/", response_model=WordInfoOutputData)
def translate_word(request: TranslateRequest):
    model = get_chat_model(request.api_key)
    chain = translation_prompt | model | StrOutputParser()
    try:
        res = chain.invoke({"language": request.language, "word": request.word, "sentence": request.sentence})
    except Exception as e:
        raise HTTPException(status_code=500, detail="Problem in generating message. " + str(e))
    return {"output": res}

@router.post("/word/info/", response_model=TranslateOutputData)
def word_info(request: WordInfoRequest):
    model = get_chat_model(request.api_key)
    chain = word_info_prompt | model | StrOutputParser()
    try:
        res = chain.invoke({"word": request.word, "sentence": request.sentence})
    except Exception as e:
        raise HTTPException(status_code=500, detail="Problem in generating message. " + str(e))
    return {"output": res}


