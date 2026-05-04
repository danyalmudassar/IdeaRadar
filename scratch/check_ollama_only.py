import os
import time
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

load_dotenv()

ollama_key = os.environ.get("OLLAMA_API_KEY")
ollama_base = os.environ.get("OLLAMA_BASE_URL", "https://dany00786-ollama.hf.space")

print(f"Testing Ollama Cloud Bridge at: {ollama_base}")
print(f"Using Model: nemotron-3-nano:30b-cloud")

try:
    # Match the logic in invoke_llm
    llm = ChatOpenAI(
        model="nemotron-3-nano:30b-cloud",
        temperature=0.1,
        openai_api_key=ollama_key,
        openai_api_base=ollama_base,
        default_headers={"Authorization": f"Bearer {ollama_key}"}
    )
    
    start = time.time()
    response = llm.invoke([HumanMessage(content="What is your name and architecture?")])
    end = time.time()
    
    print("\n✅ CONNECTION SUCCESSFUL!")
    print(f"Response: {response.content}")
    print(f"Response Time: {end - start:.2f}s")
except Exception as e:
    print(f"\n❌ CONNECTION FAILED: {e}")
