import requests
import os
import json
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

documents = [
    "Acupuncture is effective for back pain and muscle tension",
    "Yoga helps reduce stress and improve flexibility",
    "Massage therapy relieves chronic pain and improves circulation",
    "Our clinic is open Monday to Friday, 9am to 6pm",
    "We accept most major insurance plans"
]

# Embeddings  JSON file store 
print("Documents store done...")
db = []
for i, doc in enumerate(documents):
    embedding = get_embedding(doc)
    db.append({"id": i, "text": doc, "embedding": embedding})
    print(f"  Document {i+1} stored ✓")

# JSON file- save as
with open("vector_db.json", "w") as f:
    json.dump(db, f)

print("\nDatabase saved!")

# Query 
query = "back pain treatment"
query_embedding = get_embedding(query)

# find relevant document 
scores = []
for item in db:
    score = cosine_similarity(query_embedding, item["embedding"])
    scores.append((score, item["text"]))

scores.sort(reverse=True)

print(f"\nQuery: '{query}'")
print("\nClosest relevant:")
for score, text in scores[:2]:
    print(f"  {score:.3f} → {text}")