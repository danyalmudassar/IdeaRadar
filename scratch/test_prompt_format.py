import os
import requests
from dotenv import load_dotenv

load_dotenv()

url = "https://dany00786-ollama.hf.space/chat"
key = os.getenv("OLLAMA_API_KEY")

headers = {
    "Authorization": f"Bearer {key}",
    "Content-Type": "application/json"
}

# Trying the Ollama /api/generate style format
data = {
    "model": "nemotron-3-nano:30b-cloud",
    "prompt": "Say hello in 5 words",
    "stream": False
}

print(f"Testing Cloud Bridge with 'prompt' field...")
try:
    response = requests.post(url, headers=headers, json=data, timeout=30)
    print(f"Status Code: {response.status_code}")
    print(f"Body: {response.text}")
except Exception as e:
    print(f"Error: {e}")
