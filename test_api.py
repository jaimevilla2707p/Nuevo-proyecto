import requests
import json
import sys

API_KEY = "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"

def test_call(model):
    print(f"Testing: {model}")
    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "HTTP-Referer": "http://localhost:8501",
                "X-Title": "Kumis del Balcon",
                "Content-Type": "application/json"
            },
            json={
                "model": model,
                "messages": [
                    {"role": "user", "content": "Dime 'hola'"}
                ]
            }
        )
        print(f"Status: {response.status_code}")
        print(f"Body: {response.text}")
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    test_call("meta-llama/llama-3.2-3b-instruct:free")
