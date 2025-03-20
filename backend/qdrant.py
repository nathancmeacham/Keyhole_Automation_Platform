# Keyhole_Automation_Platform\backend\qdrant.py
import uuid  # ✅ Fix: Ensure uuid is imported
from qdrant_client import QdrantClient
from qdrant_client.models import ScoredPoint, VectorParams, Distance, PointStruct, SearchRequest
import time

class QdrantMemory:
    def __init__(self, host="localhost", port=6333, collection_name="rag_memory"):
        """Initialize Qdrant client and ensure the collection exists."""
        self.client = QdrantClient(host=host, port=port)
        self.collection_name = collection_name
        self._ensure_collection()

    def _ensure_collection(self):
        """Ensure the Qdrant collection exists, or create it."""
        collections = self.client.get_collections()
        if self.collection_name not in [col.name for col in collections.collections]:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=3072, distance=Distance.COSINE),  # ✅ Matches expected vector size
            )
            print(f"✅ Created Qdrant collection: {self.collection_name}")

    def store_message(self, message):
        """Stores a message in Qdrant and forces a refresh to ensure retrieval consistency."""
        
        message_id = str(uuid.uuid4())  # ✅ Generate a unique ID
        vector = self._embed_text(message)  # ✅ Convert text to vector

        point = PointStruct(
            id=message_id,
            vector=vector,
            payload={"text": message}
        )

        self.client.upsert(
            collection_name="rag_memory",
            points=[point],
            wait=True  # ✅ Ensures immediate commit
        )

        # ✅ Force Qdrant to clear previous data and refresh
        self.client.update_collection(
            collection_name="rag_memory",
            optimizer_config={"default_segment_number": 1}  # ✅ Forces refresh
        )

        print(f"✅ Stored message: {message} with ID: {message_id}")
        print(f"🔹 Stored vector: {vector[:5]}...")

        return message_id




    def search_memory(self, query, top_k=1):
        """Retrieve relevant past messages based on vector similarity."""
        
        query_vector = self._embed_text(query)  # ✅ Convert text query to vector
        
        results = self.client.query_points(
            collection_name="rag_memory",
            query=query_vector,  # ✅ Use 'query' instead of 'query_vector'
            limit=top_k,
            with_payload=True
        )

        print(f"🔍 Debugging - Query Vector: {query_vector[:5]}...")  # Debug first 5 values
        print(f"🔍 Debugging - Raw Qdrant Response: {results}")  

        if not results.points:  # ✅ Ensure results exist
            return ["No payload found"]

        return [hit.payload["text"] for hit in results.points]  # ✅ Access payload correctly



    def _embed_text(self, text: str):
        """Convert text to a vector representation (Placeholder: Replace with actual embedding model)."""
        return [0.1] * 3072  # ✅ Ensures correct vector size

if __name__ == "__main__":
    memory = QdrantMemory()

    # ✅ Store a test message
    memory.store_message("Hello, this is a test message.")

    # ✅ Search for a message
    results = memory.search_memory("test")
    print("Search results:", results)
