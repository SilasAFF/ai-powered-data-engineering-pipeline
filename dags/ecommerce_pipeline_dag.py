from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator

# Import project modules
from etl.extract.extract_fakestore_api import main as extract_main
from etl.transform.transform_users import transform_users
from etl.transform.transform_products import transform_products
from etl.transform.transform_carts import transform_carts
from etl.load.load_to_postgres import (
    load_dim_users,
    load_dim_products,
    load_fact_sales,
)
from ai.insight_generator import main as generate_ai_insights


default_args = {
    "owner": "data_engineer",
    "retries": 2,
    "retry_delay": timedelta(minutes=1),
}


with DAG(
    dag_id="ecommerce_data_pipeline",
    default_args=default_args,
    description="End-to-end e-commerce data pipeline with AI insights",
    start_date=datetime(2024, 1, 1),
    schedule_interval="@daily",
    catchup=False,
    tags=["portfolio", "data-engineering", "ai"],
) as dag:

    extract_task = PythonOperator(
        task_id="extract_api_data",
        python_callable=extract_main,
    )

    transform_users_task = PythonOperator(
        task_id="transform_users",
        python_callable=transform_users,
    )

    transform_products_task = PythonOperator(
        task_id="transform_products",
        python_callable=transform_products,
    )

    transform_carts_task = PythonOperator(
        task_id="transform_carts",
        python_callable=transform_carts,
    )

    load_users_task = PythonOperator(
        task_id="load_dim_users",
        python_callable=load_dim_users,
    )

    load_products_task = PythonOperator(
        task_id="load_dim_products",
        python_callable=load_dim_products,
    )

    load_sales_task = PythonOperator(
        task_id="load_fact_sales",
        python_callable=load_fact_sales,
    )

    ai_insights_task = PythonOperator(
        task_id="generate_ai_insights",
        python_callable=generate_ai_insights,
    )

    # ==========================
    # Task Dependencies
    # ==========================

    extract_task >> transform_users_task
    extract_task >> transform_products_task
    extract_task >> transform_carts_task

    transform_users_task >> load_users_task
    transform_products_task >> load_products_task
    transform_carts_task >> load_sales_task

    [load_users_task, load_products_task, load_sales_task] >> ai_insights_task
