import requests
import json
import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables if available
load_dotenv()

def get_api_key():
    """Retrieves the OpenRouter API key from Streamlit secrets or environment variables."""
    if "OPENROUTER_API_KEY" in st.secrets:
        return st.secrets["OPENROUTER_API_KEY"]
    return os.getenv("OPENROUTER_API_KEY", "")

def call_openrouter(prompt=None, system_context="", model="google/gemini-2.0-flash-exp:free", manual_api_key="", messages=None):
    """
    Calls the OpenRouter API with fallback logic and message history support.
    """
    api_key = manual_api_key if manual_api_key else get_api_key()
    
    if not api_key:
        return "⚠️ Error: API Key no configurada. Por favor, revisa st.secrets o tu archivo .env."

    models = [
        model,
        "meta-llama/llama-3.2-3b-instruct",
        "mistralai/mistral-7b-instruct-v0.1"
    ]
    
    # Ensure the model provided is first in the list if not already
    if model not in models:
        models.insert(0, model)

    data_body = {
        "model": "",
        "messages": []
    }
    
    # Prep the base conversation
    if messages:
        # Use provided history list
        data_body["messages"] = [{"role": "system", "content": system_context}] + messages
    else:
        # Fallback to single prompt mode
        data_body["messages"] = [
            {"role": "system", "content": system_context},
            {"role": "user", "content": prompt}
        ]

    last_error = ""
    for current_model in models:
        try:
            data_body["model"] = current_model
            response = requests.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "HTTP-Referer": "https://kumis-del-balcon.streamlit.app",
                    "X-Title": "Kumis del Balcon",
                    "Content-Type": "application/json"
                },
                data=json.dumps(data_body),
                timeout=15
            )
            
            if response.status_code == 200:
                res_json = response.json()
                if 'choices' in res_json and len(res_json['choices']) > 0:
                    return res_json['choices'][0]['message']['content']
            else:
                last_error = f"Error {response.status_code}: {response.text}"
        except Exception as e:
            last_error = str(e)
            continue
    
    return f"Muuu... tuve problemas técnicos ({last_error}). 🐮"
