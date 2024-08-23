from langchain.prompts import PromptTemplate

translation_message = (
    "You are a quick dictionary. Translate the following word into {language}. "
    "Only reply with the answer.\n\n"
    "Word: {word}\n"
    "Context Sentence: {sentence}\n"
    "Translation: "
)

translation_prompt = PromptTemplate(
    input_variables=["word", "sentence", "language"],
    template=translation_message
)