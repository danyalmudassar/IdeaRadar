import os
import time
import json
from dotenv import load_dotenv
from src.graph import app as graph_app

load_dotenv()

# Simulate a full scan for "AI Content Tools"
initial_state = {
    "topic": "AI Content Verification Tools",
    "founder_profile": {
        "location": "Global",
        "skills": "Python, LLMs",
        "budget": "$100 - $1,000",
        "time": "10-20 hrs"
    },
    "model_usage": {}
}

config = {"configurable": {"thread_id": "test_run_123"}}

print("--- Starting Full Pipeline Intelligence Scan ---")
print(f"Topic: {initial_state['topic']}")

try:
    # We will run until we hit 'ask_human' or 'END'
    # To keep it short for the trace, we will just run the first few nodes
    
    for output in graph_app.stream(initial_state, config=config):
        for key, value in output.items():
            if key != "__interrupt__":
                usage = value.get("model_usage", {})
                current_model = usage.get(key.capitalize()) or usage.get(key)
                model_tag = f"[{current_model}]" if current_model else "[N/A - API/Scraper]"
                print(f"✅ {key.upper()} {model_tag} completed.")
        
        # Check if we should stop
        state = graph_app.get_state(config)
        if state.next and state.next[0] == "ask_human":
            print("\n✋ Pipeline paused at Human Intervention (Analyst finished).")
            break

    print("\n--- System Model Usage Log (Traceback) ---")
    if os.path.exists("model_usage.log"):
        with open("model_usage.log", "r") as f:
            print(f.read())
    else:
        print("model_usage.log not found. (Check if invoke_llm was actually called)")

except Exception as e:
    print(f"\n❌ Pipeline Failure: {e}")
    import traceback
    traceback.print_exc()
