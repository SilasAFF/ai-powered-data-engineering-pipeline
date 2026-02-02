import psycopg2
import pandas as pd
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

def get_postgres_connection():
    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
        database=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD")
    )

def load_dim_users():
    """
    Loads dim_users.csv into analytics_dw.dim_users table using bulk insert.
    """
    conn = get_postgres_connection()
    cursor = conn.cursor()

    try:
        file_path = Path("data/processed/dim_users.csv")
        df = pd.read_csv(file_path)

        insert_query = """
            INSERT INTO analytics_dw.dim_users (
                user_id,
                email,
                username,
                password,
                phone,
                first_name,
                last_name,
                city,
                zipcode
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (user_id) DO NOTHING;
        """

        data = [
            (
                int(row.user_id),
                row.email,
                row.username,
                row.password,
                row.phone,
                row.first_name,
                row.last_name,
                row.city,
                row.zipcode
            )
            for row in df.itertuples(index=False)
        ]

        cursor.executemany(insert_query, data)
        conn.commit()

        print(f"dim_users loaded successfully ({len(data)} records).")

    except Exception as e:
        conn.rollback()
        print("Error loading dim_users:", e)
        raise

    finally:
        cursor.close()
        conn.close()

def load_dim_products():
    """
    Loads dim_products.csv into analytics_dw.dim_products table using bulk insert.
    """
    conn = get_postgres_connection()
    cursor = conn.cursor()

    try:
        file_path = Path("data/processed/dim_products.csv")
        df = pd.read_csv(file_path)

        insert_query = """
            INSERT INTO analytics_dw.dim_products (
                product_id,
                title,
                price,
                description,
                category,
                image,
                rating_score,
                rating_count
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (product_id) DO NOTHING;
        """

        data = [
            (
                int(row.product_id),
                row.title,
                float(row.price),
                row.description,
                row.category,
                row.image,
                float(row.rating_score),
                int(row.rating_count)
            )
            for row in df.itertuples(index=False)
        ]

        cursor.executemany(insert_query, data)
        conn.commit()

        print(f"dim_products loaded successfully ({len(data)} records).")

    except Exception as e:
        conn.rollback()
        print("Error loading dim_products:", e)
        raise

    finally:
        cursor.close()
        conn.close()

def load_fact_sales():
    """
    Loads fact_sales.csv into analytics_dw.fact_sales table using bulk insert.
    """
    conn = get_postgres_connection()
    cursor = conn.cursor()

    try:
        file_path = Path("data/processed/fact_sales.csv")
        df = pd.read_csv(file_path)

        insert_query = """
            INSERT INTO analytics_dw.fact_sales (
                order_id,
                user_id,
                order_date,
                product_id,
                quantity
            ) VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT DO NOTHING;
        """

        data = [
            (
                int(row.order_id),
                int(row.user_id),
                row.order_date,
                int(row.product_id),
                int(row.quantity)
            )
            for row in df.itertuples(index=False)
        ]

        cursor.executemany(insert_query, data)
        conn.commit()

        print(f"fact_sales loaded successfully ({len(data)} records).")

    except Exception as e:
        conn.rollback()
        print("Error loading fact_sales:", e)
        raise

    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    load_dim_users()
    load_dim_products()
    load_fact_sales()