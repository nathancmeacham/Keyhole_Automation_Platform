

# memory_manager.py


from qdrant_client.http.models import Distance, VectorParams, Filter, FieldCondition, MatchValue
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
import os
from dotenv import load_dotenv

load_dotenv()

QDRANT_URL = os.getenv("QDRANT_URL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

embeddings = OpenAIEmbeddings(model="text-embedding-3-large", openai_api_key=OPENAI_API_KEY)
qdrant_client = QdrantClient(url=QDRANT_URL)

collection_name = "rag_memory"

def init_memory_collection():
    if collection_name not in [c.name for c in qdrant_client.get_collections().collections]:
        qdrant_client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=3072, distance=Distance.COSINE)
        )

def store_memory(text, metadata):
    vectorstore = QdrantVectorStore(client=qdrant_client, collection_name=collection_name, embedding=embeddings)
    vectorstore.add_texts([text], metadatas=[metadata])

def retrieve_memory(query, memory_type=None, top_k=5):
    vectorstore = QdrantVectorStore(client=qdrant_client, collection_name=collection_name, embedding=embeddings)
    
    if memory_type:
        qdrant_filter = Filter(
            must=[FieldCondition(key="metadata.type", match=MatchValue(value=memory_type))]
        )
        return vectorstore.similarity_search(query, k=top_k, filter=qdrant_filter)
    
    return vectorstore.similarity_search(query, k=top_k)

def store_fact(key, value):
    text = f"{key}: {value}"
    metadata = {"type": "project_fact", "key": key}
    store_memory(text, metadata)

def retrieve_fact(key):
    vectorstore = QdrantVectorStore(client=qdrant_client, collection_name=collection_name, embedding=embeddings)
    qdrant_filter = Filter(
        must=[FieldCondition(key="metadata.key", match=MatchValue(value=key))]
    )
    results = vectorstore.similarity_search(key, k=1, filter=qdrant_filter)
    if results:
        return results[0].page_content.split(": ", 1)[1]
    return None