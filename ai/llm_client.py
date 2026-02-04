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


def generate_executive_insights(kpi_payload: dict) -> str:
    """
    Sends KPI data to LLM and returns executive-level insights.
    Gracefully handles API errors and quota limits.
    """
    system_prompt = load_system_prompt()

    try:
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

    except RateLimitError:
        return (
            "⚠️ Executive Summary temporarily unavailable due to API quota limits.\n"
            "The KPI data was successfully processed and is ready for analysis."
        )

    except OpenAIError as e:
        return (
            f"⚠️ AI insight generation failed due to an API error.\n"
            f"Details: {str(e)}"
        )
