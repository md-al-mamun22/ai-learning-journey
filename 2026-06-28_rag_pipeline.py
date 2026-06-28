import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")

# ============ AI FUNCTIONS ============

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

def ask_llm(question, context):
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
                    "content": f"""You are a helpful assistant for Sunrise Wellness Clinic.
Answer the question using ONLY the context below.
If the answer is not in the context, say 'I don't have that information.'

Context:
{context}"""
                },
                {
                    "role": "user",
                    "content": question
                }
            ]
        }
    )
    return response.json()["choices"][0]["message"]["content"]

# ============ STEP 1: INDEX ============

documents = [
    "Acupuncture is effective for back pain and muscle tension. Sessions are 45 minutes.",
    "Yoga classes help reduce stress and improve flexibility. We offer morning and evening classes.",
    "Massage therapy relieves chronic pain and improves blood circulation.",
    "Our clinic is open Monday to Friday, 9am to 6pm. Saturday 10am to 4pm.",
    "We accept most major insurance plans including BlueCross and Aetna.",
    "New patient consultation is free for the first visit."
]

print("📚 Step 1: Documents index done...")
db = []
for i, doc in enumerate(documents):
    embedding = get_embedding(doc)
    db.append({"id": i, "text": doc, "embedding": embedding})
    print(f"  ✓ Document {i+1} indexed")

# ============ STEP 2: RETRIEVE + GENERATE ============

print("\n🤖 RAG Chatbot ready! 'quit' write stop.\n")

while True:
    question = input("You: ")

    if question.lower() == "quit":
        break

    # Retrieve
    question_embedding = get_embedding(question)
    scores = []
    for item in db:
        score = cosine_similarity(question_embedding, item["embedding"])
        scores.append((score, item["text"]))
    scores.sort(reverse=True)
    top_docs = [text for _, text in scores[:2]]
    context = "\n".join(top_docs)

    # Generate
    answer = ask_llm(question, context)
    print(f"Bot: {answer}\n")