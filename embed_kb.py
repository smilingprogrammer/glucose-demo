from google import genai
import json
import time

# You need to install the google-generativeai package:
# pip install google-generativeai

# === CONFIGURATION ===
GEMINI_API_KEY = "AIzaSyBlzEHw55pLzMEcWBZjjL5Y1GoFbEZzweo"  # <-- Replace with your Gemini API key
KB_PATH = "glucose_knowledge_base.json"
EMBEDDINGS_PATH = "glucose_kb_embeddings.json"

# === SETUP ===
client = genai.Client(api_key=GEMINI_API_KEY)

# === LOAD KNOWLEDGE BASE ===
with open(KB_PATH, "r", encoding="utf-8") as f:
    kb = json.load(f)

# === EMBED EACH CHUNK ===
embeddings = []
for entry in kb:
    content = entry["content"]
    section = entry["section"]
    # Call Gemini Embeddings API
    result = client.models.embed_content(
        model="gemini-embedding-001",
        contents=content
    )
    embedding = result.embeddings[0].values
    embeddings.append({
        "section": section,
        "content": content,
        "embedding": embedding
    })
    time.sleep(0.2)  # Be polite to the API (adjust as needed)

# === SAVE EMBEDDINGS ===
with open(EMBEDDINGS_PATH, "w", encoding="utf-8") as f:
    json.dump(embeddings, f, indent=2)

print(f"Saved {len(embeddings)} embeddings to {EMBEDDINGS_PATH}")

# Instructions:
# 1. Replace 'YOUR_GEMINI_API_KEY_HERE' with your actual Gemini API key.
# 2. Run this script to generate and save embeddings for your knowledge base. 