import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")

def call_ai(messages):
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "openrouter/auto",
            "messages": messages
        }
    )
    return response.json()["choices"][0]["message"]["content"]

def extract_client_info(message):
    result = call_ai([
        {
            "role": "system",
            "content": """Extract client info and return ONLY JSON:
{"name": "string", "problem": "string", "urgency": "low/medium/high"}
No markdown, no extra text."""
        },
        {"role": "user", "content": message}
    ])
    result = result.strip()
    if result.startswith("```"):
        result = result.split("```")[1]
        if result.startswith("json"):
            result = result[4:]
    try:
        return json.loads(result.strip())
    except:
        return None

# Main chatbot
conversation = [
    {
        "role": "system",
        "content": """You are a caring assistant for Sunrise Wellness Clinic.
Only answer health, nutrition, and wellness questions.
Be warm, professional, and helpful.
If asked anything unrelated, politely decline."""
    }
]

print("=" * 40)
print("Sunrise Wellness Clinic — AI Assistant")
print("=" * 40)
print("Type 'quit' to exit\n")

while True:
    user_input = input("You: ")

    if user_input.lower() == "quit":
        break

    # Extract client info from first message
    if len(conversation) == 1:
        info = extract_client_info(user_input)
        if info:
            print(f"\n📋 Client Info Captured:")
            print(f"   Name: {info.get('name', 'Unknown')}")
            print(f"   Problem: {info.get('problem', 'Unknown')}")
            print(f"   Urgency: {info.get('urgency', 'Unknown')}\n")

    conversation.append({"role": "user", "content": user_input})
    reply = call_ai(conversation)
    conversation.append({"role": "assistant", "content": reply})

    print(f"Bot: {reply}\n")