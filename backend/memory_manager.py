# memory_manager.py

from qdrant_client.http.models import Distance, VectorParams, Filter, FieldCondition, MatchValue
from qdrant_client import QdrantClient
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
import os
from dotenv import load_dotenv

load_dotenv()

QDRANT_URL = os.getenv("QDRANT_URL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Ensure API key and Qdrant URL are set
if not QDRANT_URL:
    raise ValueError("⚠️ QDRANT_URL is not set in .env file!")

if not OPENAI_API_KEY:
    raise ValueError("⚠️ OPENAI_API_KEY is not set in .env file!")

# Initialize Qdrant Client and OpenAI Embeddings
try:
    qdrant_client = QdrantClient(url=QDRANT_URL)
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large", openai_api_key=OPENAI_API_KEY)
except Exception as e:
    raise ConnectionError(f"❌ Failed to initialize Qdrant or OpenAI Embeddings: {str(e)}")

# Collection Names
COLLECTION_MEMORY = "rag_memory"
COLLECTION_FACTS = "facts"


def init_memory_collection():
    """Ensure the `rag_memory` collection exists in Qdrant."""
    try:
        existing_collections = [c.name for c in qdrant_client.get_collections().collections]
        if COLLECTION_MEMORY not in existing_collections:
            qdrant_client.create_collection(
                collection_name=COLLECTION_MEMORY,
                vectors_config=VectorParams(size=3072, distance=Distance.COSINE)
            )
            print(f"✅ Collection '{COLLECTION_MEMORY}' created.")
        else:
            print(f"✅ Collection '{COLLECTION_MEMORY}' already exists.")
    except Exception as e:
        print(f"❌ Error initializing '{COLLECTION_MEMORY}': {str(e)}")


def init_fact_collection():
    """Ensure the `facts` collection exists in Qdrant with the correct dimensions."""
    try:
        existing_collections = [c.name for c in qdrant_client.get_collections().collections]

        if COLLECTION_FACTS in existing_collections:
            # Fetch the collection info to check dimensions
            collection_info = qdrant_client.get_collection(COLLECTION_FACTS)

            if collection_info.config.params.vectors.size != 3072:
                print("⚠️ Dimension mismatch detected in 'facts' collection. Recreating...")
                qdrant_client.delete_collection(COLLECTION_FACTS)

                qdrant_client.create_collection(
                    collection_name=COLLECTION_FACTS,
                    vectors_config=VectorParams(size=3072, distance=Distance.COSINE)
                )
                print(f"✅ Collection '{COLLECTION_FACTS}' recreated with correct dimensions (3072).")
            else:
                print(f"✅ Collection '{COLLECTION_FACTS}' exists with correct dimensions.")
        else:
            qdrant_client.create_collection(
                collection_name=COLLECTION_FACTS,
                vectors_config=VectorParams(size=3072, distance=Distance.COSINE)
            )
            print(f"✅ Collection '{COLLECTION_FACTS}' created.")

    except Exception as e:
        print(f"❌ Error initializing '{COLLECTION_FACTS}': {str(e)}")


def store_memory(text, metadata):
    """Store conversational memory in Qdrant."""
    try:
        vectorstore = QdrantVectorStore(client=qdrant_client, collection_name=COLLECTION_MEMORY, embedding=embeddings)
        vectorstore.add_texts([text], metadatas=[metadata])
    except Exception as e:
        print(f"❌ Error storing memory: {str(e)}")


def retrieve_memory(query, memory_type=None, top_k=5):
    """Retrieve past conversation history based on query similarity."""
    try:
        vectorstore = QdrantVectorStore(client=qdrant_client, collection_name=COLLECTION_MEMORY, embedding=embeddings)
        
        if memory_type:
            qdrant_filter = Filter(
                must=[FieldCondition(key="metadata.type", match=MatchValue(value=memory_type))]
            )
            return vectorstore.similarity_search(query, k=top_k, filter=qdrant_filter)
        
        return vectorstore.similarity_search(query, k=top_k)
    except Exception as e:
        print(f"❌ Error retrieving memory: {str(e)}")
        return []


def store_fact(key, value):
    """Store a persistent fact in Qdrant."""
    try:
        vectorstore = QdrantVectorStore(client=qdrant_client, collection_name=COLLECTION_FACTS, embedding=embeddings)
        vectorstore.add_texts([f"{key}: {value}"], metadatas={"fact_key": key})
        print(f"✅ Stored fact: {key} -> {value}")
    except Exception as e:
        print(f"❌ Error storing fact '{key}': {str(e)}")


def retrieve_fact(key):
    """Retrieve a stored fact from Qdrant."""
    try:
        vectorstore = QdrantVectorStore(client=qdrant_client, collection_name=COLLECTION_FACTS, embedding=embeddings)
        search_results = vectorstore.similarity_search(f"{key}", k=1)
        
        if search_results:
            return search_results[0].page_content.split(": ", 1)[1]  # Extract value
        
        return None
    except Exception as e:
        print(f"❌ Error retrieving fact '{key}': {str(e)}")
        return None


# 🔹 Ensure collections are created at startup
init_memory_collection()
init_fact_collection()
