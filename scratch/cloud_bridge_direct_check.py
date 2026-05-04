import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

# THE CLOUD URL
url = "https://dany00786-ollama.hf.space/chat"
key = os.getenv("OLLAMA_API_KEY")

headers = {
    "Authorization": f"Bearer {key}",
    "Content-Type": "application/json"
}

data = {
    "model": "nemotron-3-nano:30b-cloud",
    "messages": [{"role": "user", "content": "hi"}],
    "stream": False
}

print(f"--- Dedicated Cloud Bridge Diagnostic ---")
print(f"Testing URL: {url}")

try:
    response = requests.post(url, headers=headers, json=data, timeout=30)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        print("\n✅ CLOUD BRIDGE IS WORKING!")
        print(f"Response: {response.json().get('choices', [{}])[0].get('message', {}).get('content')}")
    else:
        print(f"\n❌ CLOUD BRIDGE RETURNED ERROR: {response.status_code}")
        print(f"Body: {response.text[:200]}")
except Exception as e:
    print(f"\n❌ CLITICAL FAILURE CONNECTING TO CLOUD: {e}")
