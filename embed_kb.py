from google import genai
import json
import time


GEMINI_API_KEY = "YOUR_GEMINI_API_KEY_HERE"
KB_PATH = "glucose_knowledge_base.json"
EMBEDDINGS_PATH = "glucose_kb_embeddings.json"

client = genai.Client(api_key=GEMINI_API_KEY)

with open(KB_PATH, "r", encoding="utf-8") as f:
    kb = json.load(f)

embeddings = []
for entry in kb:
    content = entry["content"]
    section = entry["section"]

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
    time.sleep(0.2)


with open(EMBEDDINGS_PATH, "w", encoding="utf-8") as f:
    json.dump(embeddings, f, indent=2)

print(f"Saved {len(embeddings)} embeddings to {EMBEDDINGS_PATH}")
