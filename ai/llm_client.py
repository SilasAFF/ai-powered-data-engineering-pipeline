import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

PROMPT_PATH = Path("ai/prompts/executive_insights.txt")

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def load_system_prompt() -> str:
    with open(PROMPT_PATH, "r", encoding="utf-8") as f:
        return f.read()


def generate_executive_insights(kpi_payload: dict) -> str:
    """
    Sends KPI data to LLM and returns executive-level insights.
    """
    system_prompt = load_system_prompt()

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": f"Here is the KPI data:\n{kpi_payload}"
            }
        ],
        temperature=0.3
    )

    return response.choices[0].message.content.strip()
