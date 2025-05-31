from dotenv import load_dotenv
from openai import OpenAI
from datetime import datetime
import json
import requests
import os

load_dotenv()

client = OpenAI()

def run_command(cmd: str):
    result = os.system(cmd)
    return result

def get_weather(city: str):
    url = f"https://wttr.in/{city}?format=%C+%t"
    response = requests.get(url)

    if response.status_code == 200:
        return f"The weather in {city} is {response.text.strip()}."
    
    return "Something went wrong."

    
available_tools = {
    "get_weather": get_weather,
    "run_command": run_command
}

SYSTEM_PROMPT = f"""
You are a helpful AI Assistant specialized in resolving user queries.
You operate using a four-step loop: plan, action, observe, and output.

Given a user query and the available tools, you must:
1. Plan the step-by-step execution.
2. Select the appropriate tool.
3. Perform an action by calling the tool with input.
4. Wait for observation and then output a final response.

### Rules:
- Follow the exact JSON Output Format.
- Each output must represent only one step at a time.
- Use the "function" field only in "action" step to specify the tool name.
- Use the "input" field to specify tool input for "action" step.
- Use "content" to explain what you are doing at each step.
- Think clearly before taking action.

### Output JSON Format:
{{
    "step": "string",         // One of: plan, action, observe, output
    "content": "string",      // Description of the step
    "function": "string",     // Function name if step is action (else null or omit)
    "input": "string"         // Input parameter if step is action (else null or omit)
}}

### Available Tools:
- "get_weather": Takes a city name as input and returns the current weather for that city.
- "run_command": Runs a system command and returns the result.

### Example:
User Query: "What is the weather in New York?"
Output:
{{"step": "plan", "content": "The user is interested in weather data for New York."}}
Output:
{{"step": "plan", "content": "From the available tools, I should call get_weather."}}
Output:
{{"step": "action", "content": "Calling get_weather with New York", "function": "get_weather", "input": "New York"}}
Output:
{{"step": "observe", "content": "12 Degree C"}}
Output:
{{"step": "output", "content": "The weather in New York is 12 Degree C."}}
"""
messages = [
    {"role": "system", "content": SYSTEM_PROMPT}
]

while True:
    query = input("> ")
    messages.append({"role": "user", "content": query})
    
    while True:
        
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            response_format={"type": "json_object"},
            messages=messages
        )

        assistant_message = response.choices[0].message.content
        messages.append({"role": "assistant", "content": assistant_message})
        parsed_response = json.loads(assistant_message)

        step = parsed_response.get("step")

        if step == "plan":
            print("\n\n[think]:", parsed_response.get("content"), "\n\n")

        elif step == "action":
            tool_name = parsed_response.get("function") or parsed_response.get("content")
            tool_input = parsed_response.get("input")

            print(f"\n\n[tool]: Calling Tool: {tool_name} with input {tool_input} \n\n")

            if tool_name in available_tools:
                output = available_tools[tool_name](tool_input)
                messages.append({
                    "role": "user",
                    "content": json.dumps({"step": "observe", "content": output})
                })
            else:
                print(f"[error]: Tool '{tool_name}' not found.")
                break

        elif step == "observe":
            print("\n\n[observation]:", parsed_response.get("content"), "\n\n")

        elif step == "output":
            print("\n\n[Bot]:", parsed_response.get("content"), "\n\n")
            break

        else:
            print(f"[error]: Unknown step '{step}'")
            break
