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

    # Find latest (most recent) path partition and reads the file products.json
    partitions = [p for p in raw_base_path.iterdir() if p.is_dir()]
    latest_partition = max(partitions)

    raw_path = latest_partition / "products.json"


    # Load raw data
    with open(raw_path, "r", encoding="utf-8") as file:
        products = json.load(file)

    # TODO: Transform data (next step)

    print("Products transformation script initialized.")


if __name__ == "__main__":
    transform_products()
