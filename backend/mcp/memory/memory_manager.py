# Keyhole_Automation_Platform\backend\mcp\memory\memory_manager.py



from qdrant_client.http.models import Distance, VectorParams, Filter, FieldCondition, MatchValue
from qdrant_client import QdrantClient
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
import os
from dotenv import load_dotenv

load_dotenv()

QDRANT_URL = os.getenv("QDRANT_URL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

EMBEDDING_DIMENSIONS = 3072  # ✅ Ensure the same embedding size across collections
embeddings = OpenAIEmbeddings(model="text-embedding-3-large", openai_api_key=OPENAI_API_KEY)
qdrant_client = QdrantClient(url=QDRANT_URL)

COLLECTION_MEMORY = "rag_memory"
COLLECTION_FACTS = "facts"


def recreate_collection(collection_name, vector_size):
    """Recreate a Qdrant collection with the correct vector size."""
    if collection_name in [c.name for c in qdrant_client.get_collections().collections]:
        qdrant_client.delete_collection(collection_name=collection_name)  # 🔹 Remove old collection

    qdrant_client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE)
    )
    print(f"✅ Qdrant '{collection_name}' collection created with {vector_size} dimensions.")


def init_memory_collection():
    """Ensure the `rag_memory` collection exists without deleting existing data."""
    existing_collections = [c.name for c in qdrant_client.get_collections().collections]

    if COLLECTION_MEMORY not in existing_collections:
        qdrant_client.create_collection(
            collection_name=COLLECTION_MEMORY,
            vectors_config=VectorParams(size=EMBEDDING_DIMENSIONS, distance=Distance.COSINE)
        )
        print(f"✅ Qdrant '{COLLECTION_MEMORY}' collection created with {EMBEDDING_DIMENSIONS} dimensions.")
    else:
        print(f"✅ Qdrant '{COLLECTION_MEMORY}' collection already exists. Skipping recreation.")



def init_fact_collection():
    """Ensure the `facts` collection exists without recreating it each time."""
    existing_collections = [c.name for c in qdrant_client.get_collections().collections]
    
    if COLLECTION_FACTS not in existing_collections:
        qdrant_client.create_collection(
            collection_name=COLLECTION_FACTS,
            vectors_config=VectorParams(size=EMBEDDING_DIMENSIONS, distance=Distance.COSINE)
        )
        print(f"✅ Qdrant '{COLLECTION_FACTS}' collection created with {EMBEDDING_DIMENSIONS} dimensions.")
    else:
        print(f"✅ Qdrant '{COLLECTION_FACTS}' collection already exists. Skipping recreation.")



def store_memory(text, metadata):
    """Store interaction memory in Qdrant."""
    vectorstore = QdrantVectorStore(client=qdrant_client, collection_name=COLLECTION_MEMORY, embedding=embeddings)
    vectorstore.add_texts([text], metadatas=[metadata])


def retrieve_memory(query, memory_type=None, top_k=5):
    """Retrieve past memory using similarity search with error handling."""
    try:
        vectorstore = QdrantVectorStore(client=qdrant_client, collection_name=COLLECTION_MEMORY, embedding=embeddings)

        if memory_type:
            qdrant_filter = Filter(
                must=[FieldCondition(key="metadata.type", match=MatchValue(value=memory_type))]
            )
            results = vectorstore.similarity_search(query, k=top_k, filter=qdrant_filter)
        else:
            results = vectorstore.similarity_search(query, k=top_k)

        return results if results else []

    except Exception as e:
        print(f"❌ Error retrieving memory: {e}")
        return []



def store_fact(key, value):
    """
    Store or update a fact in Qdrant.
    Ensure old values are deleted before storing the new one.
    """
    vectorstore = QdrantVectorStore(client=qdrant_client, collection_name=COLLECTION_FACTS, embedding=embeddings)

    # Step 1: Retrieve previous stored values
    search_results = vectorstore.similarity_search(f"{key}", k=1)

    if search_results:
        print(f"🗑️ Deleting old fact for '{key}'...")
        qdrant_client.delete(
            collection_name=COLLECTION_FACTS,
            points_selector=Filter(
                must=[FieldCondition(key="metadata.fact_key", match=MatchValue(value=key))]
            )
        )

    # Step 2: Store the new fact
    print(f"✅ Storing new fact: {key} = {value}")
    vectorstore.add_texts([f"{key}: {value}"], metadatas=[{"fact_key": key}])




def retrieve_fact(key):
    """
    Retrieve a stored fact from Qdrant using exact key filtering.
    """
    vectorstore = QdrantVectorStore(client=qdrant_client, collection_name=COLLECTION_FACTS, embedding=embeddings)

    qdrant_filter = Filter(
        must=[FieldCondition(key="metadata.fact_key", match=MatchValue(value=key))]
    )

    search_results = vectorstore.similarity_search(f"{key}", k=1, filter=qdrant_filter)

    if search_results:
        print(f"🔍 DEBUG: Retrieved facts for {key}:")
        for result in search_results:
            print(f"   - {result.page_content}")
        return search_results[0].page_content.split(": ", 1)[1]

    print(f"⚠️ DEBUG: No fact found for key: {key}")
    return None




# 🔹 Initialize both collections when the module is imported
init_memory_collection()
init_fact_collection()
