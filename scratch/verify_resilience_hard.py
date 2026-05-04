import os
import time
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from src.graph import invoke_llm

load_dotenv()

# Test Case: Force Ollama Failure via INVALID KEY and check Fallback
print("--- Resilience System Verification ---")
print("Scenario: Ollama Cloud Bridge has an INVALID API KEY.")

# Temporarily overwrite env for this process
os.environ["OLLAMA_API_KEY"] = "invalid_key_for_testing"

prompt = PromptTemplate(template="Say 'Fallback Success' if you are Gemini.", input_variables=[])

try:
    start_time = time.time()
    response, model_used = invoke_llm(prompt, {}, tier="fast")
    end_time = time.time()
    
    print(f"Model actually used: {model_used}")
    print(f"Response: {response}")
    print(f"Time taken: {end_time - start_time:.2f}s")
    
    if model_used == "gemini-2.5-pro" or model_used == "gemini-2.5-flash":
        print("\n✅ VERIFIED: Automatic Model Switch is working! It successfully pivoted to Gemini after Ollama auth failed.")
    else:
        print(f"\n❌ FAILED: It used {model_used}. Expected Gemini fallback.")
        
except Exception as e:
    print(f"\n❌ CRITICAL FAILURE: Resilience chain did not catch the error: {e}")
