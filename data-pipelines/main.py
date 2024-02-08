from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import pandas as pd
import os


def ingest_data(**kwargs):
    data = pd.DataFrame(
        {
            "timestamp": pd.date_range(start="2024-01-01", periods=1000, freq="H"),
            "value": [i * 2 for i in range(1000)],
        }
    )
    data.to_csv("/path/to/ingested_data.csv", index=False)


def clean_data(**kwargs):
    ingested_data = pd.read_csv("/path/to/ingested_data.csv")
    cleaned_data = ingested_data.drop_duplicates()
    cleaned_data.to_csv("/path/to/cleaned_data.csv", index=False)


def aggregate_data(**kwargs):
    cleaned_data = pd.read_csv("/path/to/cleaned_data.csv")
    aggregated_data = cleaned_data.groupby(cleaned_data["timestamp"].dt.date).sum()
    aggregated_data.to_csv("/path/to/aggregated_data.csv")


def analyze_data(**kwargs):
    aggregated_data = pd.read_csv("/path/to/aggregated_data.csv")


default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2024, 1, 3),
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

dag = DAG(
    "batch_processing_system",
    default_args=default_args,
    description="A batch processing system",
    schedule_interval=timedelta(days=1),
    catchup=False,
)


ingest_data_task = PythonOperator(
    task_id="ingest_data",
    python_callable=ingest_data,
    dag=dag,
)

clean_data_task = PythonOperator(
    task_id="clean_data",
    python_callable=clean_data,
    dag=dag,
)

aggregate_data_task = PythonOperator(
    task_id="aggregate_data",
    python_callable=aggregate_data,
    dag=dag,
)

analyze_data_task = PythonOperator(
    task_id="analyze_data",
    python_callable=analyze_data,
    dag=dag,
)


ingest_data_task >> clean_data_task >> aggregate_data_task >> analyze_data_task
