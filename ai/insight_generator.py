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


if __name__ == "__main__":
    df = fetch_kpi_summary()
    insights = generate_insights(df)
    save_insights(insights)
