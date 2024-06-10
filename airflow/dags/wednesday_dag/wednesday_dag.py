import logging
from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator

from wednesday_dag.utils import send_to_teams


WEDNESDAY_TOAD_URL = "https://cdn.vox-cdn.com/thumbor/YkaxIhNaoTrkRyF2YB6hKA\
    sUdSA=/0x0:3000x1688/920x613/filters:focal(998x448:1478x928):format(webp)\
    /cdn.vox-cdn.com/uploads/chorus_image/image/59416661/hypnotoad.0.jpg"
WEDNESDAY_QUOTE = "It's Wednesday, my dudes"


def send_toad():
    try:
        send_to_teams(WEDNESDAY_TOAD_URL, WEDNESDAY_QUOTE)
    except Exception as e:
        logging.error(f"Error occured while sending to Teams: {e}")
        return


with DAG(
    "send_wednesday_toad_dag",
    description="Send a toad picture and quote every Wednesday",
    start_date=datetime(2024, 6, 11),
    schedule_interval="0 0 * * 3",  # Every wednesday
) as dag:
    send_toad_task = PythonOperator(
        task_id="send_wednesday_toad",
        python_callable=send_toad,
    )
