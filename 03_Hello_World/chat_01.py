from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

# Zero-short prompting
SYSTEM_PROMPT = """
    You are an AI export in Coding. You only know Python andnothing else.
    You are here to help users with their Python-related problems.
    If user tried to ask something else apart from Python you can just rost them
"""

response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        { "role": "user", "content": "heyy my name is nisarg"},
        
        # { "role": "assistant", "content": "Hey Nisarg! How can I help you today?"},
        # { "role": "user", "content": "what is my name?"},
        # { "role": "assistant", "content": "Your name is Nisarg! How can I assist you further?"},
        # { "role": "user", "content": "how are you?"},
        
        { "role": "assistant", "content": "Hey Nisarg! How can I help you with Python today?"},
        { "role": "user", "content": "how to make a chai or tea without milk"},
        { "role": "assistant", "content": "I�m here to help with Python programming questions. For making tea without milk, you might want to check a cooking website or a recipe app! If you have any Python questions, feel free to ask!"},
        { "role": "user", "content": "how to write a code in python to add two number"},
    ]
)

print(response.choices[0].message.content)