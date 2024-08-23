from langchain.prompts import FewShotPromptTemplate, PromptTemplate

# Define the example template
example_template = """
Word: {word}
Context Sentence: {sentence}
Word Information: {word_info}
"""

# Define our examples
examples = [
    {
        "word": "Piece of cake",
        "sentence": "Finishing the project was a piece of cake.",
        "word_info": """{{
    "word": "Piece of cake",
    "definition": "A task or activity that is very easy to accomplish",
    "synonym": "Easy, Simple, Effortless",
    "example": [
        "The exam was a piece of cake, I finished it in 20 minutes",
        "Cooking this dish is a piece of cake, anyone can do it",
        "For him, solving that math problem was a piece of cake"
    ],
    "usage": "'Piece of cake' is commonly used in informal conversations to describe tasks that are very easy to complete."
}}"""
    }
]

# Create the example prompt
example_prompt = PromptTemplate(
    input_variables=["word", "sentence", "word_info"],
    template=example_template
)

# Create the few-shot prompt template
word_info_prompt = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
    prefix="Provide information about the given English word. Follow the format of the examples provided below:",
    suffix="Word: {word}\nContext Sentence: {sentence}\nWord Information: ",
    input_variables=["word", "sentence"],
    example_separator="\n\n"
)