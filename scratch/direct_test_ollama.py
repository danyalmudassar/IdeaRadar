import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()
url = "https://dany00786-ollama.hf.space/chat"
key = os.getenv("OLLAMA_API_KEY")

headers = {
    "Authorization": f"Bearer {key}",
    "Content-Type": "application/json"
}

data = {
    "model": "nemotron-3-nano:30b-cloud",
    "messages": [{"role": "user", "content": "hi"}]
}

try:
    print(f"Sending request to {url}...")
    response = requests.post(url, headers=headers, json=data, timeout=20)
    print(f"Status: {response.status_code}")
    print(f"Body: {response.text}")
except Exception as e:
    print(f"Error: {e}")
