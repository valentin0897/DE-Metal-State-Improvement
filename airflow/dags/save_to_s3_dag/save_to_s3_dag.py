import logging
from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator

from save_to_s3_dag.utils import send_post_to_teams


default_args = {
    'depends_on_past': False,
    'start_date': datetime(2024, 6, 15),
}


def run_send_post():
    try:
        send_post_to_teams()
    except Exception as e:
        logging.error(f"Error occurred: {e}")
        raise


with DAG(
    'orchestrate_quotes_pictures_aws_dag',
    default_args=default_args,
    description='Sending post to teams and saving it to AWS',
    schedule_interval="@daily",
    catchup=False,
) as dag:

    send_task = PythonOperator(
        task_id='send_picture_and_quote_task',
        python_callable=run_send_post,
    )

start_op = EmptyOperator(task_id='start')
finish_op = EmptyOperator(task_id='finish')

start_op >> send_task >> finish_op
