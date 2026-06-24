



import requests
importos
from dotenv import load-load_dotenv
load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")
response = requests.post(
    url= "https://openrouter.ai/api/v1/chat/completions",
    headers={
        "model": "openrouter/auto",
        "messages": [
            {"role": "user", "content": "say one line, be an AI engineer is worth it?"}
        ]
    }

)
result = response.json()
print(result["choices"][0]["message"][content])