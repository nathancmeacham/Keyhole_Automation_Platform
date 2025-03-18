# fact_extractor.py (dynamic LLM from .env)
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DEFAULT_LLM_MODEL = os.getenv("DEFAULT_LLM_MODEL", "gpt-4o")

llm = ChatOpenAI(model=DEFAULT_LLM_MODEL, openai_api_key=OPENAI_API_KEY)

def extract_facts(statement):
    prompt = ChatPromptTemplate.from_template("""
    Extract structured facts from the user's statement. 
    Return facts as key-value pairs in JSON format. 
    If no clear facts are present, return an empty JSON object.

    User: "{statement}"
    Response:
    """)
    chain = prompt | llm
    response = chain.invoke({"statement": statement})
    try:
        facts = eval(response.content.strip())
        if isinstance(facts, dict):
            return facts
        else:
            return {}
    except:
        return {}