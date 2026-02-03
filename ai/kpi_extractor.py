import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()


def get_postgres_engine():
    """
    Creates a SQLAlchemy engine for PostgreSQL.
    """
    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")
    host = os.getenv("POSTGRES_HOST")
    port = os.getenv("POSTGRES_PORT")
    db = os.getenv("POSTGRES_DB")

    connection_url = (
        f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}"
    )

    return create_engine(connection_url)


def fetch_kpi_summary():
    """
    Fetches monthly KPI summary from the Data Warehouse.
    Returns a pandas DataFrame.
    """
    query = """
        SELECT
            month,
            total_orders,
            total_units_sold,
            total_revenue,
            average_order_value
        FROM analytics_dw.v_kpi_summary
        ORDER BY month;
    """

    engine = get_postgres_engine()

  
    with engine.connect() as connection:
        df = pd.read_sql(query, connection)

    return df


if __name__ == "__main__":
    df = fetch_kpi_summary()
    print(df)
