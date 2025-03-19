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
    """Ensure the `rag_memory` collection exists with the correct vector size."""
    recreate_collection(COLLECTION_MEMORY, EMBEDDING_DIMENSIONS)


def init_fact_collection():
    """Ensure the `facts` collection exists with the correct vector size."""
    recreate_collection(COLLECTION_FACTS, EMBEDDING_DIMENSIONS)


def store_memory(text, metadata):
    """Store interaction memory in Qdrant."""
    vectorstore = QdrantVectorStore(client=qdrant_client, collection_name=COLLECTION_MEMORY, embedding=embeddings)
    vectorstore.add_texts([text], metadatas=[metadata])


def retrieve_memory(query, memory_type=None, top_k=5):
    """Retrieve past memory using similarity search."""
    vectorstore = QdrantVectorStore(client=qdrant_client, collection_name=COLLECTION_MEMORY, embedding=embeddings)

    if memory_type:
        qdrant_filter = Filter(
            must=[FieldCondition(key="metadata.type", match=MatchValue(value=memory_type))]
        )
        return vectorstore.similarity_search(query, k=top_k, filter=qdrant_filter)

    return vectorstore.similarity_search(query, k=top_k)


def store_fact(key, value):
    """Store a fact in Qdrant."""
    vectorstore = QdrantVectorStore(client=qdrant_client, collection_name=COLLECTION_FACTS, embedding=embeddings)
    
    # ✅ Ensure metadata is a LIST of dictionaries
    vectorstore.add_texts([f"{key}: {value}"], metadatas=[{"fact_key": key}])


def retrieve_fact(key):
    """Retrieve a stored fact from Qdrant."""
    vectorstore = QdrantVectorStore(client=qdrant_client, collection_name=COLLECTION_FACTS, embedding=embeddings)

    try:
        search_results = vectorstore.similarity_search(key, k=1)
        if search_results:
            fact_text = search_results[0].page_content
            if ": " in fact_text:
                return fact_text.split(": ", 1)[1].strip()  # ✅ Extract the fact value safely
        return None
    except Exception as e:
        print(f"❌ Error retrieving fact '{key}': {str(e)}")
        return None


# 🔹 Initialize both collections when the module is imported
init_memory_collection()
init_fact_collection()
