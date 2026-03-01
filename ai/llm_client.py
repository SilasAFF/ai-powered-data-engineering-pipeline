import os
from dotenv import load_dotenv
from openai import OpenAI, OpenAIError, RateLimitError

load_dotenv()


def get_openai_client():
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError("OPENAI_API_KEY is not set.")

    return OpenAI(api_key=api_key)


def generate_executive_insights(payload: dict) -> str:
    """
    Generates executive insights using OpenAI.
    Client is instantiated lazily to avoid DAG import failures.
    """
    client = get_openai_client()

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

    content = response.choices[0].message.content
    if content is None:
        raise ValueError("OpenAI returned empty response content")
    return content
