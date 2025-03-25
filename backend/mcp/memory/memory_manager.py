# Keyhole_Automation_Platform\backend\mcp\memory\memory_manager.py

import os
import traceback
from dotenv import load_dotenv
from hashlib import md5
from qdrant_client import QdrantClient
from qdrant_client.http.models import (
    Distance,
    VectorParams,
    Filter,
    FieldCondition,
    MatchValue,
    PointStruct,
)
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore

load_dotenv()

QDRANT_URL = os.getenv("QDRANT_URL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

EMBEDDING_DIMENSIONS = 3072

class MemoryManager:
    def __init__(self):
        print("🔧 Initializing MemoryManager...")
        print("🔍 MemoryManager stack trace:")
        traceback.print_stack(limit=5)

        self.embeddings = OpenAIEmbeddings(
            model="text-embedding-3-large", openai_api_key=OPENAI_API_KEY
        )
        self.qdrant_client = QdrantClient(url=QDRANT_URL)
        self.COLLECTION_MEMORY = "rag_memory"
        self.COLLECTION_FACTS = "facts"

        self.ensure_collection(self.COLLECTION_MEMORY, EMBEDDING_DIMENSIONS)
        self.ensure_collection(self.COLLECTION_FACTS, EMBEDDING_DIMENSIONS)

    def ensure_collection(self, name, vector_size):
        try:
            collections = self.qdrant_client.get_collections().collections
            collection_names = [c.name for c in collections]

            if name in collection_names:
                print(f"✅ Collection '{name}' already exists. Skipping creation.")
            else:
                self.qdrant_client.create_collection(
                    collection_name=name,
                    vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
                )
                print(f"✅ Created new collection '{name}' with {vector_size} dimensions.")

        except Exception as e:
            print(f"❌ Error checking or creating collection '{name}': {e}")

    def recreate_collection(self, *args, **kwargs):    raise RuntimeError("🚨 recreate_collection was called unexpectedly!")


    def init_memory_collection(self):
        collections = [
            c.name for c in self.qdrant_client.get_collections().collections
        ]
        if self.COLLECTION_MEMORY not in collections:
            self.recreate_collection(self.COLLECTION_MEMORY, EMBEDDING_DIMENSIONS)
        else:
            print(
                f"✅ Qdrant '{self.COLLECTION_MEMORY}' collection already exists. Skipping recreation."
            )

    def init_fact_collection(self):
        collections = [
            c.name for c in self.qdrant_client.get_collections().collections
        ]
        if self.COLLECTION_FACTS not in collections:
            self.recreate_collection(self.COLLECTION_FACTS, EMBEDDING_DIMENSIONS)
        else:
            print(
                f"✅ Qdrant '{self.COLLECTION_FACTS}' collection already exists. Skipping recreation."
            )

    def store_memory(self, text, metadata):
        try:
            vectorstore = QdrantVectorStore(
                client=self.qdrant_client,
                collection_name=self.COLLECTION_MEMORY,
                embedding=self.embeddings,
            )
            vectorstore.add_texts([text], metadatas=[metadata])
            print(f"✅ Stored memory: {text[:30]}...")
        except Exception as e:
            print(f"❌ Failed to store memory: {e}")

    def retrieve_memory(self, query, memory_type=None, top_k=5):
        try:
            vectorstore = QdrantVectorStore(
                client=self.qdrant_client,
                collection_name=self.COLLECTION_MEMORY,
                embedding=self.embeddings,
            )

            qdrant_filter = None
            if memory_type:
                qdrant_filter = Filter(
                    must=[
                        FieldCondition(
                            key="metadata.type", match=MatchValue(value=memory_type)
                        )
                    ]
                )

            results = vectorstore.similarity_search(query, k=top_k, filter=qdrant_filter)
            return results if results else []
        except Exception as e:
            print(f"❌ Error retrieving memory: {e}")
            return []

    def store_fact(self, key, value):
        try:
            point_id = int(md5(key.encode()).hexdigest()[:8], 16)
            vector = self.embeddings.embed_query(f"{key}: {value}")

            self.qdrant_client.upsert(
                collection_name=self.COLLECTION_FACTS,
                points=[
                    PointStruct(
                        id=point_id,
                        vector=vector,
                        payload={
                            "fact_key": key,
                            "text": f"{key}: {value}"
                        },
                    )
                ],
            )
            print(f"✅ Stored fact: {key} = {value} (ID: {point_id})")
        except Exception as e:
            print(f"❌ Failed to store fact: {e}")

    def retrieve_fact(self, key):
        try:
            point_id = int(md5(key.encode()).hexdigest()[:8], 16)
            result = self.qdrant_client.retrieve(
                collection_name=self.COLLECTION_FACTS,
                ids=[point_id]
            )
            if result and len(result) > 0:
                value = result[0].payload.get("text", "").split(": ", 1)[1]
                print(f"🔍 Retrieved fact for '{key}': {value}")
                return value

            print(f"⚠️ No fact found for key: {key}")
            return None

        except Exception as e:
            print(f"❌ Error retrieving fact: {e}")
            return None

    def list_all_facts(self):
        try:
            response, _ = self.qdrant_client.scroll(
                collection_name=self.COLLECTION_FACTS,
                with_payload=True,
                limit=1000
            )

            facts = {}
            for point in response:
                payload = point.payload or {}
                text = payload.get("text", "")
                if ": " in text:
                    key, value = text.split(": ", 1)
                    facts[key] = value

            return facts

        except Exception as e:
            print(f"❌ Error listing all facts: {e}")
            return {}
