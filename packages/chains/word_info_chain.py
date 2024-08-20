from langchain_core.output_parsers import StrOutputParser
from packages.models import openai
from packages.prompts import word_info_prompt

word_info_chain = word_info_prompt | openai | StrOutputParser()

if __name__ == "__main__":
    res = word_info_chain.invoke({"word": "Utterly"})
    print(res)