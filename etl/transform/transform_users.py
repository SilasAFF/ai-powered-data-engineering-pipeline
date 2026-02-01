import json
import pandas as pd
from pathlib import Path


def transform_users():
    """
    Transforms raw users data into a clean dim_users dataset.
    """
    processed_path = Path("data/processed")
    processed_path.mkdir(parents=True, exist_ok=True)

    raw_base_path = Path("data/raw/users")

    # Find latest (most recent) path partition directory
    partitions = [p for p in raw_base_path.iterdir() if p.is_dir()]
    latest_partition = max(partitions)

    raw_path = latest_partition / "users.json"

    # Load raw data
    with open(raw_path, "r", encoding="utf-8") as file:
        users = json.load(file)

    # Create DataFrame
    df = pd.DataFrame(users)

    # Flatten name
    name_df = pd.json_normalize(df["name"])
    name_df.columns = ["first_name", "last_name"]

    # Flatten address
    address_df = pd.json_normalize(df["address"])
    address_df = address_df[["city", "zipcode"]]

    # Combine all columns removing nested columns "name","address" and adding their respective derivatives
    df = pd.concat(
        [
            df.drop(columns=["name", "address","__v"]),
            name_df,
            address_df
        ],
        axis=1
    )

    # Rename primary key
    df = df.rename(columns={"id": "user_id"})

    # Standardize strings
    df["email"] = df["email"].str.lower()
    df["username"] = df["username"].str.lower()
    df["first_name"] = df["first_name"].str.lower()
    df["last_name"] = df["last_name"].str.lower()
    df["city"] = df["city"].str.lower()

    # Ensure correct data types
    df["user_id"] = df["user_id"].astype(int)
    df["zipcode"] = df["zipcode"].astype(str)

    # Save processed data
    output_path = processed_path / "dim_users.csv"
    df.to_csv(output_path, index=False)


    print("Users transformation script initialized.")


if __name__ == "__main__":
    transform_users()
