import json
from pathlib import Path

import pandas as pd

from ai.kpi_extractor import fetch_kpi_summary
from ai.llm_client import generate_executive_insights
from ai.llm_client_local import generate_executive_insights_local


def generate_insights(df: pd.DataFrame) -> dict:
    """
    Generates structured, rule-based KPI insights.
    This is the single source of truth for business logic.
    """
    df = df.sort_values("month")

    first = df.iloc[0]
    last = df.iloc[-1]

    revenue_change_pct = (
        (last["total_revenue"] - first["total_revenue"]) / first["total_revenue"]
    ) * 100

    aov_change_pct = (
        (last["average_order_value"] - first["average_order_value"])
        / first["average_order_value"]
    ) * 100

    orders_change_pct = (
        (last["total_orders"] - first["total_orders"]) / first["total_orders"]
    ) * 100

    insights = []
    alerts = []

    if aov_change_pct < -50:
        alerts.append("Sharp AOV decrease (>50%) detected")
        insights.append("Significant drop in average order value")

    if revenue_change_pct < 0 and orders_change_pct > 0:
        insights.append("Revenue decline driven primarily by lower ticket size")

    if not insights:
        insights.append("Stable performance with no critical anomalies detected")

    return {
        "period": f"{first['month']} → {last['month']}",
        "metrics": {
            "revenue_change_pct": round(revenue_change_pct, 2),
            "aov_change_pct": round(aov_change_pct, 2),
            "orders_change_pct": round(orders_change_pct, 2),
        },
        "insights": insights,
        "alerts": alerts,
    }


def structured_insights_to_text(insights: dict) -> str:
    """
    Converts structured KPI insights into a human-readable executive summary.
    Used as the final deterministic fallback when no LLM is available.
    """
    lines = []

    lines.append(f"Performance period: {insights['period']}.")

    metrics = insights["metrics"]
    lines.append(
        f"Revenue changed by {metrics['revenue_change_pct']}%, "
        f"average order value by {metrics['aov_change_pct']}%, "
        f"and order volume by {metrics['orders_change_pct']}%."
    )

    if insights["insights"]:
        lines.append("Key insights:")
        for item in insights["insights"]:
            lines.append(f"- {item}")

    if insights["alerts"]:
        lines.append("Alerts:")
        for alert in insights["alerts"]:
            lines.append(f"- {alert}")

    return "\n".join(lines)


def save_insights(payload: dict):
    """
    Persists structured insights to disk (machine-readable output).
    """
    output_dir = Path("ai/outputs")
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / "kpi_insights.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=4)

    print(f"Insights saved at {output_path}")


def dataframe_to_llm_payload(df: pd.DataFrame) -> dict:
    """
    Converts DataFrame to a JSON-safe payload for LLMs.
    """
    df_copy = df.copy()

    if "month" in df_copy.columns:
        df_copy["month"] = df_copy["month"].astype(str)

    return {
        "periods": df_copy.to_dict(orient="records")
    }


def generate_llm_insights(payload: dict) -> str:
    """
    Generates executive insights using a cloud-based LLM.
    """
    return generate_executive_insights(payload)


if __name__ == "__main__":
    df = fetch_kpi_summary()

    # 1. Deterministic, rule-based insights (source of truth)
    structured_insights = generate_insights(df)
    save_insights(structured_insights)

    # Prepare JSON-safe payload once
    llm_payload = dataframe_to_llm_payload(df)

    # 2. Executive summary generation (LLM with fallbacks)
    try:
        # Cloud LLM (OpenAI)
        executive_text = generate_llm_insights(llm_payload)

    except Exception as openai_error:
        print("⚠️ OpenAI failed:", repr(openai_error))

        try:
            # Local LLM (Ollama)
            executive_text = generate_executive_insights_local(llm_payload)

        except Exception as ollama_error:
            print("❌ Ollama failed:", repr(ollama_error))

            # Final deterministic fallback
            executive_text = structured_insights_to_text(structured_insights)

    # 3. Persist executive summary
    output_path = Path("ai/outputs/executive_summary.txt")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(executive_text)

    print(f"Executive summary saved at {output_path}")



def main():
    df = fetch_kpi_summary()

    structured_insights = generate_insights(df)
    save_insights(structured_insights)

    llm_payload = dataframe_to_llm_payload(df)

    try:
        executive_text = generate_llm_insights(llm_payload)
    except Exception:
        try:
            executive_text = generate_executive_insights_local(llm_payload)
        except Exception:
            executive_text = structured_insights_to_text(structured_insights)

    output_path = Path("ai/outputs/executive_summary.txt")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(executive_text)

    print("Executive summary generated successfully.")
