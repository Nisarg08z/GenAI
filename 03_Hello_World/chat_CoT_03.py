from dotenv import load_dotenv
from openai import OpenAI
import json

load_dotenv()

client = OpenAI()

# Chain Of Thought: The model is encouraged to break down reasoning step by step before arriving at an answer. 
SYSTEM_PROMPT = """
    you are an helpfull AI assistant who is specialized in resolving user query.
    For the given user input, analyse the input and break down the problem step by step.
    The steps are you get a user input, you analyse, you think, you think again, and think for several times and then return the output with an explanation.
    You are not allowed to give a direct answer. You have to break down the problem into smaller
    sub-problems and then solve them one by one.
    
    Rules:
    1. Follow the strict JSON output as per schema.
    2. Always perform one step at a time and wait for the next input.
    3. carefully analyse the user query,
    
    output Format:
    {{"step": "string", "content": "string"}}

    Example:
    Input: what is 2 + 2
    Output: {{"step": "analyse", "content": "Alight! The user is interest in maths query and he is asking a basic arthematic operation}}
    Output: {{"step": "think", "content": "I need to break down the problem into smaller sub-problems. I need to identify the operation and the numbers involved."}}
    Output: {{"step": "output", "content": "4"}}
    Output: {{"step": "validate", "content": "seems like 4 is correct ans for 2 + 2"}}
    Output: {{"step": "result", "content": "2 + 2 = 4 and this is calculated by adding all numbers"}}
    
    Example:
    Input: what is 2 + 2 * 5 / 3
    Output: {{"step": "analyse", "content": "Alight! The user is interest in maths query and he is asking a basic arthematic operation}}
    Output: {{"step": "think", "content": "To perform this addition, I must use BODMAS rule."}}
    Output: {{"step": "validate", "content": "Correct, using BODMAS is the right approach here"}}
    Output: {{"step": "think", "content": "first i need to solve division that is 5 / 3 which gives 1.666666666667."}}
    Output: {{"step": "validate", "content": "Correct, using BODMAS the division must be performed"}}
    Output: {{"step": "think", "content": "Now as i have already solved 5 / 3 now the equation looks like 2 + 2 * 1.666666666667"}}
    Output: {{"step": "validate", "content": "yes, new equation is absolutely correct"}}
    Output: {{"step": "think", "content": "the equation looks like 2 + 2 * 1.666666666667"}}
    and so on..........
    
"""

# response = client.chat.completions.create(
#     model="gpt-4.1-mini",
#     response_format={"type": "json_object"},
#     messages=[
#         {"role": "system", "content": SYSTEM_PROMPT},
#         {"role": "user", "content": "what is 5 / 2 * 3 to the power 4"},
#         { "role": "assistant", "content": json.dumps({"step": "analyse", "content": "The user is asking to evaluate a mathematical expression involving division, multiplication, and exponentiation: 5 / 2 * 3^4."})},
#         { "role": "assistant", "content": json.dumps({"step": "think", "content": "I need to recall the order of operations (PEMDAS/BODMAS). Exponentiation should be calculated first, then multiplication and division from left to right."})},
#         { "role": "assistant", "content": json.dumps({"step": "think again", "content": "First, calculate 3 to the power 4 which is 3^4 = 3 * 3 * 3 * 3 = 81. Then, proceed with the division and multiplication from left to right: 5 / 2 * 81."})},
#         { "role": "assistant", "content": json.dumps({"step": "next step", "content": "Now, calculate 5 divided by 2, which is 2.5. Then multiply this result by 81."})},
#         { "role": "assistant", "content": json.dumps({"step": "final calculation", "content": "2.5 multiplied by 81 equals 202.5."})},
#         { "role": "assistant", "content": json.dumps({"step": "result", "content": "The value of the expression 5 / 2 * 3^4 is 202.5."})},
        
        

#     ]
# )

# print("\n\n[Bot]:", response.choices[0].message.content, "\n\n")

messages = [
    {"role": "system", "content": SYSTEM_PROMPT},
]

query = input("> ")
messages.append({"role": "user", "content": query})

while True:
    response = client.chat.completions.create(
        model="gpt-4.1",
        response_format={"type": "json_object"},
        messages=messages
    )
    
    messages.append({"role": "assistant", "content": response.choices[0].message.content})
    parsed_response = json.loads(response.choices[0].message.content)
    
    if parsed_response.get("step") == "think":
        # make a claude api call and append the result as validate
        messages.append({"role": "assistant", "content": "<>"})
        continue
        
    
    if parsed_response.get("step") != "result":
        print("\n\n[think]:", parsed_response.get("content"), "\n\n")
        continue
    
    print("\n\n[Bot]:", parsed_response.get("content"), "\n\n")
    break
