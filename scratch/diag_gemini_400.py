import os
import json
import time
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage

load_dotenv()
key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")

try:
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-pro", google_api_key=key, temperature=0.1)
    # Try a simple prompt with a system message to match the graph's behavior
    messages = [
        SystemMessage(content="You are a helpful assistant."),
        HumanMessage(content="Explain the 400 INVALID_ARGUMENT error in Gemini API.")
    ]
    resp = llm.invoke(messages)
    print(f"Response: {resp.content}")
except Exception as e:
    print(f"Full Error: {e}")
