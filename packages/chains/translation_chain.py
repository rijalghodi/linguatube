from langchain_core.output_parsers import StrOutputParser
from packages.models import openai
from packages.prompts import translation_prompt

translation_chain = translation_prompt | openai | StrOutputParser()

if __name__ == "__main__":
    res = translation_chain.invoke({"language": "Indonesian", "word": "Dreadful"})
    print(res)