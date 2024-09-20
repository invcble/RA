import json
import time
from together import Together
from flask import Flask, request, jsonify
from dotenv import load_dotenv

from google_api import google_search as web_search

load_dotenv()

app = Flask(__name__)
client = Together()

def create_context(query_list):
    context = ""

    for query in query_list:
        result = web_search(query)
        context += f"Sub_Question: {query} \n Search_result: {result}  \n\n"

    return context


def call_agent(context: str, message_prompt: list,
               max_tokens: int = None,
               temperature: float = None,
               top_p: float = None,
               repetition_penalty: float = None
               ):
    
    messages = message_prompt
    messages.extend([
        {
            "role": "system",
            "content": context
        }
    ])

    arguments = {
        "messages": messages,
        "model": 'meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo',
    }

    if max_tokens is not None:
        arguments["max_tokens"] = max_tokens
    if temperature is not None:
        arguments["temperature"] = temperature
    if top_p is not None:
        arguments["top_p"] = top_p
    if repetition_penalty is not None:
        arguments["repetition_penalty"] = repetition_penalty

    print(arguments)

    # Call the Together API with the arguments
    chat_completion = client.chat.completions.create(**arguments)
    response = chat_completion.choices[0].message

    return response.content

# Flask route to handle API requests
@app.route('/api/v1/call_agent', methods=['POST'])
def handle_call_agent():
    data = request.json
    
    query_list = data.get("query_list", [])
    message_prompt = data.get("llm_payload", {}).get("message_prompt", [])
    max_tokens = data.get("llm_payload", {}).get("max_tokens", None)
    temperature = data.get("llm_payload", {}).get("temperature", None)
    top_p = data.get("llm_payload", {}).get("top_p", None)
    repetition_penalty = data.get("llm_payload", {}).get("repetition_penalty", None)

    context = create_context(query_list)
    response = call_agent(context, message_prompt, max_tokens, temperature, top_p, repetition_penalty)
    
    return jsonify(response)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
