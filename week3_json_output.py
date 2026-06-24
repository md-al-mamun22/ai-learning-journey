import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")

def extract_client_info(client_message):
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "openrouter/auto",
            "messages": [
                {
                    "role": "system",
                    "content": """You are a data extraction assistant. 
                    Extract information from the client message and return ONLY a JSON object with these fields:
                    - name (string)
                    - problem (string)
                    - urgency (low/medium/high)
                    
                    Return ONLY the JSON, no other text."""
                },
                {
                    "role": "user",
                    "content": client_message
                }
            ]
        }
    )
    
    result = response.json()["choices"][0]["message"]["content"]
    return json.loads(result)

# Test
message = "Hi, my name is Sarah. I have been having severe back pain for 3 days and can barely walk."
data = extract_client_info(message)

print("Extracted Data:")
print(f"Name: {data['name']}")
print(f"Problem: {data['problem']}")
print(f"Urgency: {data['urgency']}")