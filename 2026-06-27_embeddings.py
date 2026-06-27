import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")

def get_embedding(text):
    response = requests.post(
        url="https://openrouter.ai/api/v1/embeddings",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "openai/text-embedding-3-small",
            "input": text
        }
    )
    return response.json()["data"][0]["embedding"]

def cosine_similarity(vec1, vec2):
    dot = sum(a*b for a, b in zip(vec1, vec2))
    mag1 = sum(a**2 for a in vec1) ** 0.5
    mag2 = sum(b**2 for b in vec2) ** 0.5
    return dot / (mag1 * mag2)

# বাক্যগুলো
sentences = [
    "I have severe back pain",
    "My back is hurting a lot",
    "I want to book an appointment",
    "I need to schedule a visit",
    "What are your clinic hours?",
    "I love playing football"
]

# Query
query = "back pain treatment"
print(f"Query: '{query}'\n")

query_emb = get_embedding(query)

print("Similarity scores:")
for sentence in sentences:
    emb = get_embedding(sentence)
    score = cosine_similarity(query_emb, emb)
    print(f"  {score:.3f} — {sentence}")