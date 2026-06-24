import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")

messages = [
    {
        "role": "system",
"content": "You are a helpful assistant for Sunrise Wellness Clinic. Only answer questions related to health, nutrition, and wellness. If someone asks anything unrelated, politely say you can only help with wellness topics."    }
]

print("Wellness Bot ready! 'quit' likhle bondho hobe.")
print ("You are a helpful assistant for Sunrise Wellness Clinic...")

while True:
    user_input = input("Tumi: ")
    
    if user_input.lower() == "quit":
        break
    
    messages.append({"role": "user", "content": user_input})
    
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
    
    reply = response.json()["choices"][0]["message"]["content"]
    messages.append({"role": "assistant", "content": reply})
    
    print(f"Bot: {reply}\n")