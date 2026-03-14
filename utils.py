import requests
import json
import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables if available
load_dotenv()

def get_api_key():
    """Retrieves the OpenRouter API key from Streamlit secrets or environment variables."""
    try:
        if "OPENROUTER_API_KEY" in st.secrets:
            return st.secrets["OPENROUTER_API_KEY"]
    except Exception:
        pass
    return os.getenv("OPENROUTER_API_KEY", "")

def call_openrouter(prompt=None, system_context="", model="google/gemini-2.0-flash-lite-preview-02-05:free", manual_api_key="", messages=None):
    """
    Calls the OpenRouter API with fallback logic and message history support.
    - Uses free-tier model IDs with the correct :free suffix.
    - Falls back through multiple models if the primary fails.
    - Timeout set to 30s to handle slow free-tier responses.
    """
    api_key = manual_api_key if manual_api_key else get_api_key()
    
    if not api_key:
        return "⚠️ Error: API Key no configurada. Por favor, revisa st.secrets o tu archivo .env."

    # Free-tier models confirmed working on OpenRouter (tested 2026-03-01).
    # Order matters: best quality first, lightest models last as final fallbacks.
    fallback_models = [
        "mistralai/mistral-small-3.1-24b-instruct:free",  # Best quality (may hit 429 under load)
        "meta-llama/llama-3.2-3b-instruct:free",          # Widely available
        "google/gemma-3-e4b-it:free",                     # Updated Gemini-family model
        "cognitivecomputations/dolphin3.0-r1-mistral-24b:free", 
        "liquid/lfm-2.5-1.2b-instruct:free",               # Fast lightweight fallback ✅
        "nvidia/nemotron-nano-9b-v2:free",                  # Final fallback ✅
    ]

    # Build the final ordered list: requested model first, then fallbacks (no duplicates)
    models = [model] + [m for m in fallback_models if m != model]

    # Build the base message payload
    if messages:
        # Use provided conversation history (already contains the latest user message)
        base_messages = [{"role": "system", "content": system_context}] + messages
    else:
        # Single-turn fallback
        base_messages = [
            {"role": "system", "content": system_context},
            {"role": "user", "content": prompt or ""},
        ]

    last_error = ""
    for current_model in models:
        try:
            payload = {
                "model": current_model,
                "messages": base_messages,
                "temperature": 0.7,        # Conversational but focused
                "max_tokens": 512,         # Keep responses concise
                "stream": True,            # Empezar a mandar palabras rápido
            }
            response = requests.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "HTTP-Referer": "https://kumis-del-balcon.streamlit.app",
                    "X-Title": "Kumis del Balcon",
                    "Content-Type": "application/json",
                },
                data=json.dumps(payload),
                timeout=30,  # Increased from 15s — free-tier models can be slow
                stream=True, # Enable Server-Sent Events
            )

            if response.status_code == 200:
                def generator():
                    for line in response.iter_lines():
                        if line:
                            line_str = line.decode('utf-8')
                            if line_str.startswith('data: '):
                                data_str = line_str[6:]
                                if data_str == '[DONE]':
                                    break
                                try:
                                    data_json = json.loads(data_str)
                                    if "choices" in data_json and len(data_json["choices"]) > 0:
                                        delta = data_json["choices"][0].get("delta", {})
                                        if "content" in delta:
                                            yield delta["content"]
                                except Exception:
                                    pass
                return generator()
            elif response.status_code == 429:
                last_error = f"Modelo {current_model}: límite de tasa alcanzado (429)."
            elif response.status_code == 402:
                last_error = f"Modelo {current_model}: requiere créditos (402)."
            else:
                last_error = f"Modelo {current_model}: Error {response.status_code}."

        except requests.exceptions.Timeout:
            last_error = f"Modelo {current_model}: tiempo de espera agotado."
            continue
        except Exception as e:
            last_error = f"Modelo {current_model}: {str(e)[:80]}"
            continue

    return f"Muuu... tuve problemas técnicos con todos los modelos disponibles ({last_error}). Intenta de nuevo en un momento. 🐮"
