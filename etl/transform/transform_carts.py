import json
import pandas as pd
from pathlib import Path


def transform_carts():
    """
    Transforms raw carts data into a fact_sales dataset.
    """
    print("Carts transformation script initialized.")
    
    processed_path = Path("data/processed")
    processed_path.mkdir(parents=True, exist_ok=True)

    raw_base_path = Path("data/raw/carts")

    # Find latest (most recent) path partition
    partitions = [p for p in raw_base_path.iterdir() if p.is_dir()]
    latest_partition = max(partitions)

    raw_path = latest_partition / "carts.json"

    # Load raw data
    with open(raw_path, "r", encoding="utf-8") as file:
        carts = json.load(file)


     # Create DataFrame
    df = pd.DataFrame(carts)

    # Rename columns
    df = df.rename(
        columns={
            "id": "order_id",
            "userId": "user_id"
        }
    )

    # Convert "date" column to date format
    df["order_date"] = pd.to_datetime(df["date"]).dt.date

    # Drop original "date" column
    df = df.drop(columns=["date","__v"])
   
    # Explode products (one row per product) and reset index due concatenation issues
    df = df.explode("products").reset_index(drop=True)


    # Normalize products column
    products_df = pd.json_normalize(df["products"]).reset_index(drop=True)
    products_df = products_df.rename(
        columns={
            "productId": "product_id",
            "quantity": "quantity"
        }
    )

    # Combine exploded products with main DataFrame and remove old nested column "products"
    df = pd.concat(
        [
            df.drop(columns=["products"]),
            products_df
        ],
        axis=1
    )


    # Ensure correct data types
    df["order_id"] = df["order_id"].astype(int)
    df["user_id"] = df["user_id"].astype(int)
    df["product_id"] = df["product_id"].astype(int)
    df["quantity"] = df["quantity"].astype(int)
    df["order_date"] = pd.to_datetime(df["order_date"])


    # Save processed fact table
    output_path = processed_path / "fact_sales.csv"
    df.to_csv(output_path, index=False)

    print(f"fact_sales saved at {output_path}")

if __name__ == "__main__":
    transform_carts()
