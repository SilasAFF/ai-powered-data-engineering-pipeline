import json
import pandas as pd
from pathlib import Path


def transform_products():
    """
    Transforms raw products data into a clean dim_products dataset.
    """
    processed_path = Path("data/processed")
    processed_path.mkdir(parents=True, exist_ok=True)

    raw_base_path = Path("data/raw/products")

    # Find latest (most recent) path partition directory
    partitions = [p for p in raw_base_path.iterdir() if p.is_dir()]
    latest_partition = max(partitions)

    raw_path = latest_partition / "products.json"


    # Load raw data
    with open(raw_path, "r", encoding="utf-8") as file:
        products = json.load(file)


    # Create DataFrame
    df = pd.DataFrame(products)

    # Flatten rating column
    rating_df = pd.json_normalize(df["rating"])
    rating_df.columns = ["rating_score", "rating_count"]

    # Remove nested column "rating" and add new columns "rating_score", "rating_count"
    df = pd.concat(
        [
            df.drop(columns=["rating"]), 
            rating_df
        ], 
        axis=1
    )

    # Rename columns
    df = df.rename(columns={"id": "product_id"})

    # Ensure correct data types
    df["product_id"] = df["product_id"].astype(int)
    df["price"] = df["price"].astype(float)
    df["rating_score"] = df["rating_score"].astype(float)
    df["rating_count"] = df["rating_count"].astype(int)

    # Save processed data
    output_path = processed_path / "dim_products.csv"
    df.to_csv(output_path, index=False)

    print("Products transformation script initialized.")


if __name__ == "__main__":
    transform_products()
