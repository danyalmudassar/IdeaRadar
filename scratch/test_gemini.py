import os
import json
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

load_dotenv()
key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
print(f"Key found: {key[:10]}...")

try:
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-pro", google_api_key=key)
    resp = llm.invoke([HumanMessage(content="Hello")])
    print(f"Response: {resp.content}")
except Exception as e:
    print(f"Error: {e}")
