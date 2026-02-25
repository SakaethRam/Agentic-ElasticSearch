# =========================================================
# Storing Interaction as Memory (with embedding)
# =========================================================
from openai import OpenAI  # or your embedding provider

client = OpenAI()

def embed_and_store_interaction(query, response, session_id=None):
    text = f"Query: {query}\nResponse: {response}"
    embedding = client.embeddings.create(
        model="text-embedding-3-large", input=text
    ).data[0].embedding

    doc = {
        "content": text,
        "content_vector": embedding,
        "timestamp": "now",
        "session_id": session_id,
        "interaction_type": "conversation_turn"
    }

    es.index(index="knowledge_and_memory_index", document=doc)