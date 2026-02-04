import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
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

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False,
        },
        timeout=60,
    )

    response.raise_for_status()

    return response.json()["response"]
