import json
import numpy as np
from google import genai

GEMINI_API_KEY = "AIzaSyBlzEHw55pLzMEcWBZjjL5Y1GoFbEZzweo"
EMBEDDINGS_PATH = "glucose_kb_embeddings.json"
TOP_K = 3

client = genai.Client(api_key=GEMINI_API_KEY)

with open(EMBEDDINGS_PATH, "r", encoding="utf-8") as f:
    kb = json.load(f)

kb_vectors = np.array([entry["embedding"] for entry in kb])

def embed_query(query):
    result = client.models.embed_content(
        model="gemini-embedding-001",
        contents=query
    )
    return np.array(result.embeddings[0].values)


def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def retrieve_top_k(query_vec, k=TOP_K):
    sims = [cosine_similarity(query_vec, vec) for vec in kb_vectors]
    top_indices = np.argsort(sims)[-k:][::-1]
    return [kb[i] for i in top_indices]

def agentic_answer(user_q, history=None):
    query_vec = embed_query(user_q)
    top_chunks = retrieve_top_k(query_vec)
    context = "\n".join(f"[{c['section']}] {c['content']}" for c in top_chunks)

    history_str = ""
    if history:
        for turn in history[-5:]:  # Use last 5 turns
            history_str += f"User: {turn['user']}\nAgent: {turn['agent']}\n"

    prompt = f"""
You are Glucose, an agentic AI assistant for the Glucose product. Your job is to help users by answering their questions using ONLY the knowledge provided below.

Instructions:
- If the user's question is incomplete, ambiguous, or unclear, politely ask them to clarify or complete their question before answering. Do NOT attempt to answer until the question is clear.
- If the answer is not found in the knowledge, say: "I'm sorry, I don't have enough information to answer that based on my current knowledge. Could you clarify or ask something else?"
- If the question is clear and the answer is in the knowledge, provide a concise, structured, and helpful answer. Use bullet points or short paragraphs if appropriate.
- Always be polite, professional, and conversational.
- If the user asks about something outside the Glucose product or the provided knowledge, politely let them know you are only able to answer questions about Glucose.

Conversation so far:
{history_str}
User: {user_q}

Knowledge Base:
{context}
"""
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text


def main():
    print("Agentic Glucose AI. Type 'exit' to quit.")
    history = []
    while True:
        user_q = input("\nAsk a question: ").strip()
        if user_q.lower() in ("exit", "quit"): break
        answer = agentic_answer(user_q, history)
        print("\nAnswer:\n", answer)
        history.append({"user": user_q, "agent": answer})

if __name__ == "__main__":
    main() 