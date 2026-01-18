import os
import requests
import time
from dotenv import load_dotenv

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")
if not HF_TOKEN:
    raise ValueError("HF_TOKEN environment variable not set")

# Using a high-performance model officially supported by the v1 router
MODEL = "Qwen/Qwen2.5-7B-Instruct"
API_URL = "https://router.huggingface.co/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/json"
}

def generate_text(prompt: str) -> str:
    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "system", 
                "content": "You are a wellness planner. You MUST respond using these headers: 'DIET PLAN:', 'WORKOUT PLAN:', and 'DAILY ROUTINE ADVICE:'."
            },
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 900,
        "temperature": 0.7
    }

    for i in range(3):
        try:
            response = requests.post(API_URL, headers=HEADERS, json=payload)
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
            
            elif response.status_code in [503, 429]:
                # Model loading or rate limiting
                time.sleep(10)
                continue
            else:
                # Catching any other specific errors
                error_info = response.json()
                raise RuntimeError(f"⚠️ API Error {response.status_code}:\n{error_info}")
        
        except Exception as e:
            if i == 2: raise RuntimeError(f"Request failed: {e}")
            time.sleep(5)

    return "Error: The AI timed out."