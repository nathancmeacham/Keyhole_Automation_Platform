# Keyhole_Automation_Platform\backend\mcp\memory\qdrant_memory.py

# 🔒 ARCHIVED - Replaced by memory_manager.py
# This file is no longer used in production.

raise ImportError("This module is deprecated. Use backend.mcp.memory.memory_manager instead.")
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
from sentence_transformers import SentenceTransformer
import uuid

COLLECTION_NAME = "agent_memory"

model = SentenceTransformer("all-MiniLM-L6-v2")
client = QdrantClient(host="localhost", port=6333)

def init_memory():
    if not client.collection_exists(collection_name=COLLECTION_NAME):
        client.recreate_collection(
            collection_name=COLLECTION_NAME,
            vector_size=384,
            distance="Cosine"
        )

def embed_text(text: str):
    return model.encode(text).tolist()

def store_memory(text: str):
    embedding = embed_text(text)
    point = PointStruct(id=str(uuid.uuid4()), vector=embedding, payload={"text": text})
    client.upsert(collection_name=COLLECTION_NAME, points=[point])
    return "Memory stored."

def retrieve_memory(query: str, limit=3):
    embedding = embed_text(query)
    results = client.search(
        collection_name=COLLECTION_NAME,
        query_vector=embedding,
        limit=limit
    )
    return [hit.payload["text"] for hit in results]
