import os
import time
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from src.graph import invoke_llm

load_dotenv()

# Test Case: Force Ollama Failure and check Fallback
print("--- Resilience System Verification ---")
print("Scenario: Ollama Cloud Bridge is OFFLINE (simulated).")

# We know the cloud bridge URL returns 404 in our current environment
# invoke_llm will try Ollama first, hit 404, then move to Gemini.

prompt = PromptTemplate(template="Say 'Fallback Success' if you are Gemini.", input_variables=[])

try:
    start_time = time.time()
    # We pass an empty dict for inputs
    response, model_used = invoke_llm(prompt, {}, tier="fast")
    end_time = time.time()
    
    print(f"Model actually used: {model_used}")
    print(f"Response: {response}")
    print(f"Time taken: {end_time - start_time:.2f}s")
    
    if model_used != "nemotron-3-nano:30b-cloud":
        print("\n✅ VERIFIED: Automatic Model Switch is working! It successfully bypassed the offline Ollama bridge.")
    else:
        print("\n❌ FAILED: It stayed on Ollama (or Ollama unexpectedly worked).")
        
except Exception as e:
    print(f"\n❌ CRITICAL FAILURE: Resilience chain did not catch the error: {e}")
