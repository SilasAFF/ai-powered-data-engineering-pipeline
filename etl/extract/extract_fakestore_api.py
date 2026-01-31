import os
import json
import requests
from datetime import datetime
from dotenv import load_dotenv


# Load environment variables
load_dotenv()

RAW_DATA_PATH = os.getenv("RAW_DATA_PATH", "data/raw")

BASE_URL = "https://fakestoreapi.com"

ENDPOINTS = {
    "products": "/products",
    "users": "/users",
    "carts": "/carts"
}


def create_directory(path: str):
    if not os.path.exists(path):
        os.makedirs(path)


def extract(endpoint: str):
    url = BASE_URL + endpoint
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def save_raw_data(data, dataset_name: str):
    execution_date = datetime.now().strftime("%Y-%m-%d")

    directory = os.path.join(
        RAW_DATA_PATH,
        dataset_name,
        execution_date
    )

    create_directory(directory)

    file_path = os.path.join(
        directory,
        f"{dataset_name}.json"
    )

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

    print(f"✅ {dataset_name} saved at {file_path}")


def main():
    for dataset, endpoint in ENDPOINTS.items():
        print(f"🔄 Extracting {dataset}...")
        data = extract(endpoint)
        save_raw_data(data, dataset)


if __name__ == "__main__":
    main()
