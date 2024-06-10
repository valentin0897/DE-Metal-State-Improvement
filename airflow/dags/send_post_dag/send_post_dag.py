import logging
from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator

from send_post_dag.utils import send_post_to_teams


def run_send_post_to_teams():
    try:
        send_post_to_teams()
        logging.info("Successfully sent the picture and quote")
    except Exception as e:
        logging.error(f"Error occurred while sending picture and quote: {e}")
        raise


with DAG(
    'send_post_to_teams_dag',
    description='A DAG to orchestrate pictures and quotes sending',
    start_date=datetime(2024, 6, 11),
    schedule_interval="@daily",
    catchup=False,
) as dag:
    send_task = PythonOperator(
        task_id='send_post_to_teams',
        python_callable=run_send_post_to_teams,
    )
