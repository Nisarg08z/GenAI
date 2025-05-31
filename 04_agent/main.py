from dotenv import load_dotenv
from openai import OpenAI
from datetime import datetime

load_dotenv()

client = OpenAI()

SYSTEM_PROMPT = f"""
You are a helpful AI Assistant.

Today's date and time is {datetime.now()}.
"""

response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": "What is the date and time today"},
    ]
)

print(response.choices[0].message.content)
