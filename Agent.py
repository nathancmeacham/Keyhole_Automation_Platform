# Agent.py (dynamic LLM selection)
import logging
import init_project  # Ensure paths are set correctly
import os
from dotenv import load_dotenv
from openai import OpenAI
from qdrant_client import QdrantClient
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_qdrant import QdrantVectorStore
from langchain.chains import RetrievalQA
from memory_manager import init_memory_collection, store_memory, retrieve_memory, retrieve_fact, store_fact
from codebase_snapshot import snapshot_and_commit
from project_utils import count_files
from fact_extractor import extract_facts

# Disable all logging
logging.disable(logging.CRITICAL)

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
QDRANT_URL = os.getenv("QDRANT_URL")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-large")
DEFAULT_LLM_MODEL = os.getenv("DEFAULT_LLM_MODEL", "gpt-4o")
AVAILABLE_LLM_MODELS = os.getenv("AVAILABLE_LLM_MODELS", "gpt-4o,gpt-4-turbo,gpt-3.5-turbo").split(",")

openai_client = OpenAI(api_key=OPENAI_API_KEY)
embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL, openai_api_key=OPENAI_API_KEY)

init_memory_collection()

def select_llm_model():
    print("\nSelect the LLM model for this session:")
    for idx, model in enumerate(AVAILABLE_LLM_MODELS, start=1):
        print(f"{idx}. {model}")
    choice = input(f"Enter choice (1-{len(AVAILABLE_LLM_MODELS)}) or press Enter for default ({DEFAULT_LLM_MODEL}): ")
    try:
        if choice.strip() == "":
            return DEFAULT_LLM_MODEL
        choice_idx = int(choice) - 1
        if 0 <= choice_idx < len(AVAILABLE_LLM_MODELS):
            return AVAILABLE_LLM_MODELS[choice_idx]
        else:
            print("Invalid choice. Using default model.")
            return DEFAULT_LLM_MODEL
    except:
        print("Invalid input. Using default model.")
        return DEFAULT_LLM_MODEL

def setup_rag_chain(llm_model):
    vectorstore = QdrantVectorStore(
        client=QdrantClient(url=QDRANT_URL),
        collection_name="rag_memory",
        embedding=embeddings
    )
    llm = ChatOpenAI(model=llm_model, openai_api_key=OPENAI_API_KEY)
    qa_chain = RetrievalQA.from_chain_type(llm, retriever=vectorstore.as_retriever(), return_source_documents=False)
    return qa_chain

if __name__ == "__main__":
    llm_model = select_llm_model()
    print(f"\n🚀 Intelligent RAG Agent initialized with LLM model: {llm_model}")

    qa_chain = setup_rag_chain(llm_model)

    print("\n🚀 Intelligent RAG Agent is ready! Type 'exit' to quit.")

    while True:
        user_query = input("\nEnter your question: ")
        if user_query.lower() in ["exit", "quit"]:
            commit_choice = input("Commit Codebase to RAG? (y/n): ").lower()
            if commit_choice == 'y':
                snapshot_and_commit(commit_message="End of session snapshot")
            print("Exiting RAG Agent. Goodbye!")
            break

        # Check for stored name first
        if "my name" in user_query.lower():
            fact_value = retrieve_fact("user_name")
            if fact_value:
                answer = f"Your name is {fact_value}."
                print("\n🤖 Answer:", answer)
                continue  # Skip further processing since we have the answer
            else:
                answer = "I don't know your name yet. What should I call you?"
                print("\n🤖 Answer:", answer)
                new_name = input("Enter your name: ").strip()
                if new_name:
                    store_fact("user_name", new_name)
                    print(f"\n✅ Got it! I'll remember that your name is {new_name}.")
                continue  # Skip further processing since we've handled the name storage

        extracted_facts = extract_facts(user_query)
        if extracted_facts:
            for key, value in extracted_facts.items():
                store_fact(key, value)
            answer = "✅ Got it! I've learned the following facts:\n"
            answer += "\n".join([f"- {k.replace('_', ' ').title()}: {v}" for k, v in extracted_facts.items()])
        else:
            known_facts = ["lead_developer", "project_name", "project_purpose"]
            answered = False
            for fact_key in known_facts:
                if fact_key.replace("_", " ") in user_query.lower():
                    fact_value = retrieve_fact(fact_key)
                    if fact_value:
                        answer = f"{fact_key.replace('_', ' ').title()} is {fact_value}."
                    else:
                        answer = f"I don't know {fact_key.replace('_', ' ')} yet."
                    answered = True
                    break
                    
            if not answered:
                if "how many files" in user_query.lower():
                    num_files = count_files()
                    answer = f"There are currently {num_files} files in your project."
                else:
                    memory_context_docs = retrieve_memory(user_query, memory_type="chat_interaction", top_k=3)
                    memory_context = "\n".join([doc.page_content for doc in memory_context_docs])

                    prompt = f"""
                    You are an intelligent RAG-based assistant. Here is relevant past context:
                    {memory_context}

                    User's current question:
                    {user_query}

                    Provide a clear, concise, and helpful answer.
                    """

                    response = qa_chain.invoke({"query": prompt})
                    answer = response.get('result', 'Sorry, I could not find an answer.')

        print(f"\n🤖 Answer: {answer}")

        store_memory(
            text=f"User: {user_query}\nAgent: {answer}",
            metadata={"type": "chat_interaction"}
        )
