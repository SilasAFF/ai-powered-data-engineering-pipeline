from llm_client import generate_executive_insights
import json
from pathlib import Path
import pandas as pd
from kpi_extractor import fetch_kpi_summary


def generate_insights(df: pd.DataFrame) -> dict:
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
        insights.append(
            "Significant drop in average order value"
        )

    if revenue_change_pct < 0 and orders_change_pct > 0:
        insights.append(
            "Revenue decline driven primarily by lower ticket size"
        )

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


def save_insights(payload: dict):
    output_dir = Path("ai/outputs")
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / "kpi_insights.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=4)

    print(f"Insights saved at {output_path}")

def generate_llm_insights(kpi_df: pd.DataFrame) -> str:
    """
    Generates executive insights using a Large Language Model.
    """
    payload = {
        "periods": kpi_df.to_dict(orient="records")
    }

    return generate_executive_insights(payload)

def generate_narrative_fallback(df: pd.DataFrame) -> str:
    """
    Generates an executive narrative based on KPI trends without using LLMs.
    """
    df = df.sort_values("month")

    first = df.iloc[0]
    last = df.iloc[-1]

    revenue_delta = last["total_revenue"] - first["total_revenue"]
    revenue_pct = (revenue_delta / first["total_revenue"]) * 100

    aov_delta = last["average_order_value"] - first["average_order_value"]
    aov_pct = (aov_delta / first["average_order_value"]) * 100

    orders_delta = last["total_orders"] - first["total_orders"]
    orders_pct = (orders_delta / first["total_orders"]) * 100

    narrative = []

    narrative.append(
        f"Between {first['month']} and {last['month']}, total revenue "
        f"{'increased' if revenue_pct >= 0 else 'decreased'} by "
        f"{abs(revenue_pct):.1f}%."
    )

    narrative.append(
        f"Order volume {'grew' if orders_pct >= 0 else 'declined'} by "
        f"{abs(orders_pct):.1f}%, while average order value "
        f"{'rose' if aov_pct >= 0 else 'fell'} by "
        f"{abs(aov_pct):.1f}%."
    )

    if revenue_pct < 0 and orders_pct > 0:
        narrative.append(
            "This indicates that revenue pressure is primarily driven by "
            "a reduction in average ticket size rather than demand."
        )

    if revenue_pct > 0 and orders_pct > 0:
        narrative.append(
            "Overall performance shows healthy growth supported by both "
            "volume and revenue expansion."
        )

    return "\n".join(narrative)


if __name__ == "__main__":
    df = fetch_kpi_summary()

    # Rule-based insights
    structured_insights = generate_insights(df)
    save_insights(structured_insights)

    # LLM-based insights
    executive_text = generate_llm_insights(df)
    
    # If LLM fails, generate deterministic narrative
    if "temporarily unavailable" in executive_text.lower():
        executive_text = generate_narrative_fallback(df)
    
    output_path = Path("ai/outputs/executive_summary.txt")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(executive_text)
    
    print(f"Executive summary saved at {output_path}")


