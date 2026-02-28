import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

# Aqui está o segredo: 
# Se estiver no Docker, usaremos http://host.docker.internal:11434
# Se estiver no VS Code e não houver essa env, ele usa o localhost por padrão.
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
            timeout=120, # Aumentei um pouco o timeout porque o Llama 3 local pode demorar via Docker
        )

        response.raise_for_status()
        return response.json()["response"]
        
    except requests.exceptions.ConnectionError:
        raise Exception(f"Não foi possível conectar ao Ollama em {OLLAMA_URL}. Verifique se o Ollama está rodando e se a env OLLAMA_HOST está como 0.0.0.0 no Windows.")