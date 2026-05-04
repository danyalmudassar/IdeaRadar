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
    "messages": [{"role": "user", "content": "Say hello"}],
    "stream": False
}

print(f"Testing URL: {url}")
try:
    response = requests.post(url, headers=headers, json=data, timeout=10)
    print(f"Status Code: {response.status_code}")
    print(f"Content Type: {response.headers.get('Content-Type')}")
    print(f"Response Content Snippet: {response.text[:200]}")
except Exception as e:
    print(f"Error: {e}")
