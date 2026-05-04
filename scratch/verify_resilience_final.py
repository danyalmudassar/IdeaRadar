import os
import time
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from src.graph import invoke_llm

load_dotenv()

# Test Case: Force Ollama Failure via GARBAGE URL and check Fallback
print("--- Resilience System Verification ---")
print("Scenario: Ollama Cloud Bridge URL is GARBAGE.")

# Temporarily overwrite env
os.environ["OLLAMA_BASE_URL"] = "https://this-url-does-not-exist-at-all-123456.com"

prompt = PromptTemplate(template="Say 'Fallback Success' if you are Gemini.", input_variables=[])

try:
    start_time = time.time()
    response, model_used = invoke_llm(prompt, {}, tier="fast")
    end_time = time.time()
    
    print(f"Model actually used: {model_used}")
    print(f"Response: {response}")
    print(f"Time taken: {end_time - start_time:.2f}s")
    
    if "gemini" in model_used:
        print("\n✅ VERIFIED: Automatic Model Switch is working! It successfully pivoted to Gemini after Ollama connection failed.")
    else:
        print(f"\n❌ FAILED: It used {model_used}. Expected Gemini fallback.")
        
except Exception as e:
    print(f"\n❌ CRITICAL FAILURE: Resilience chain did not catch the error: {e}")
