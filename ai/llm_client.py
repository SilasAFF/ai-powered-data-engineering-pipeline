from openai import RateLimitError, OpenAIError
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


def generate_executive_insights(payload: dict) -> str:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a senior business analyst.",
            },
            {
                "role": "user",
                "content": f"Generate an executive summary from the following KPI data:\n{payload}",
            },
        ],
    )

    return response.choices[0].message.content

