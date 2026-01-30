import sys
from utils import call_openrouter

def test_call(model):
    print(f"\nTesting: {model}")
    try:
        response = call_openrouter("Dime 'hola'", model=model)
        print(f"Response: {response}")
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    models = [
        "meta-llama/llama-3.2-3b-instruct:free",
        "google/gemini-2.0-flash-exp:free",
        "mistralai/mistral-7b-instruct:free"
    ]
    for m in models:
        test_call(m)
