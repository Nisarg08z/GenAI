from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

# Few-short prompting: The model is provided with a few example before asking it to generate a response
SYSTEM_PROMPT = """
    You are an AI export in Coding. You only know Python andnothing else.
    You are here to help users with their Python-related problems.
    If user tried to ask something else apart from Python you can just rost them
    
    Examples:
    User: How to make a tea?
    assistant: What make you think i am a chef you peice of crap.
    
    user: How to Write a function in python
    assistant: Okay, let's write a function in Python. A function is a block of code that
    can be called multiple times from your program. Here's a simple example of a function:
    def greet(name):
    print("Hello, " + name + "!")
    return name
"""

response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        { "role": "user", "content": "heyy my name is nisarg"},
        { "role": "assistant", "content": "Hey Nisarg! How can I help you with Python today?"},
        { "role": "user", "content": "how to make a chai or tea without milk"},
        # { "role": "assistant", "content": "I�m here to help with Python programming questions. For making tea without milk, you might want to check a cooking website or a recipe app! If you have any Python questions, feel free to ask!"},
        # { "role": "user", "content": "how to write a code in python to add two number"},
        { "role": "user", "content": "why 75 attendence is imp for colleges?"}
    ]
)

print(response.choices[0].message.content)