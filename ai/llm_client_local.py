import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_URL = f"{OLLAMA_BASE_URL}/api/generate"
MODEL_NAME = "llama3:latest"

def generate_executive_insights_local(payload: dict) -> str:
    """
    Generates executive insights using a local LLM via Ollama.
    """
    prompt = f"""
You are a senior business analyst.

Based on the following KPI data, write a concise executive summary
highlighting trends, risks, and performance drivers.

KPI Data:
{json.dumps(payload, indent=2)}
"""

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False,
            },
            timeout=120,
        )

        response.raise_for_status()
        return response.json()["response"]
        
    except requests.exceptions.ConnectionError:
        raise Exception(f"Not possible to connect to Ollama at {OLLAMA_URL}. Verify that Ollama is running and that the OLLAMA_HOST environment variable is set to 0.0.0.0 on Windows.")