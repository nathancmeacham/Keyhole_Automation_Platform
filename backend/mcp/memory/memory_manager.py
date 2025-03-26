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
DEFAULT_USER_ID = "guest"

class MemoryManager:
    def __init__(self):
        print("🔧 Initializing MemoryManager...")
        print("🔍 MemoryManager stack trace:")
        traceback.print_stack(limit=5)

        self.embeddings = OpenAIEmbeddings(
            model="text-embedding-3-large", openai_api_key=OPENAI_API_KEY
        )
        self.qdrant_client = QdrantClient(url=QDRANT_URL)
        self.base_memory_collection = "rag_memory"
        self.base_facts_collection = "facts"
        self.ip_analytics_collection = "ip_analytics"

        self.ensure_collection(self.ip_analytics_collection, EMBEDDING_DIMENSIONS)

    def _get_collection_name(self, base, user_id):
        return f"{base}_{user_id}"

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

    def recreate_collection(self, *args, **kwargs):
        raise RuntimeError("🚨 recreate_collection was called unexpectedly!")

    def store_memory(self, text, metadata, user_id=DEFAULT_USER_ID):
        try:
            collection = self._get_collection_name(self.base_memory_collection, user_id)
            self.ensure_collection(collection, EMBEDDING_DIMENSIONS)
            vectorstore = QdrantVectorStore(
                client=self.qdrant_client,
                collection_name=collection,
                embedding=self.embeddings,
            )
            vectorstore.add_texts([text], metadatas=[metadata])
            print(f"✅ Stored memory for {user_id}: {text[:30]}...")
        except Exception as e:
            print(f"❌ Failed to store memory: {e}")

    def retrieve_memory(self, query, memory_type=None, top_k=5, user_id=DEFAULT_USER_ID):
        try:
            collection = self._get_collection_name(self.base_memory_collection, user_id)
            vectorstore = QdrantVectorStore(
                client=self.qdrant_client,
                collection_name=collection,
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

    def store_fact(self, key, value, user_id=DEFAULT_USER_ID):
        try:
            point_id = int(md5(f"{user_id}_{key}".encode()).hexdigest()[:8], 16)
            vector = self.embeddings.embed_query(f"{key}: {value}")
            collection = self._get_collection_name(self.base_facts_collection, user_id)
            self.ensure_collection(collection, EMBEDDING_DIMENSIONS)
            self.qdrant_client.upsert(
                collection_name=collection,
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
            print(f"✅ Stored fact for {user_id}: {key} = {value} (ID: {point_id})")
        except Exception as e:
            print(f"❌ Failed to store fact: {e}")

    def retrieve_fact(self, key, user_id=DEFAULT_USER_ID):
        try:
            point_id = int(md5(f"{user_id}_{key}".encode()).hexdigest()[:8], 16)
            collection = self._get_collection_name(self.base_facts_collection, user_id)
            result = self.qdrant_client.retrieve(
                collection_name=collection,
                ids=[point_id]
            )
            if result and len(result) > 0:
                value = result[0].payload.get("text", "").split(": ", 1)[1]
                print(f"🔍 Retrieved fact for '{key}' (user={user_id}): {value}")
                return value

            print(f"⚠️ No fact found for key: {key} (user={user_id})")
            return None

        except Exception as e:
            print(f"❌ Error retrieving fact: {e}")
            return None

    def list_all_facts(self, user_id=DEFAULT_USER_ID):
        try:
            collection = self._get_collection_name(self.base_facts_collection, user_id)
            response, _ = self.qdrant_client.scroll(
                collection_name=collection,
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

    def store_guest_ip(self, ip):
        key = f"guest_ip::{ip}"
        self.store_fact(key, "1", user_id=self.ip_analytics_collection)

    def track_guest_ip(self, ip):
        """Alias for test clarity — ensures one call style."""
        self.store_guest_ip(ip)

    def list_guest_ips(self):
        return [
            k.split("::")[-1]
            for k in self.list_all_facts(user_id=self.ip_analytics_collection).keys()
            if k.startswith("guest_ip::")
        ]

    def track_user_ip(self, user_id, ip):
        """Only stores a new IP for a user if it doesn't already exist."""
        key = f"user_ip::{user_id}::{ip}"
        point_id = int(md5(f"{self.ip_analytics_collection}_{key}".encode()).hexdigest()[:8], 16)

        # Check if point already exists before storing
        result = self.qdrant_client.retrieve(
            collection_name=self._get_collection_name(self.base_facts_collection, self.ip_analytics_collection),
            ids=[point_id]
        )

        if not result:
            self.store_fact(key, "1", user_id=self.ip_analytics_collection)

    def get_user_ips(self, user_id):
        return [
            k.split("::")[-1]
            for k in self.list_all_facts(user_id=self.ip_analytics_collection).keys()
            if k.startswith(f"user_ip::{user_id}::")
        ]
