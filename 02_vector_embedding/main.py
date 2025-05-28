from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

Client = OpenAI()

text = "Dog chases cat"

response = Client.embeddings.create(
    model="text-embedding-3-small",
    input=text
)

print(response)