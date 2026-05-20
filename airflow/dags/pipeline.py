from airflow import DAG

from airflow.operators.python import PythonOperator

from datetime import datetime
from datetime import timedelta

from clickhouse_driver import Client

import random
import time


default_args = {

    "owner": "airflow",

    "depends_on_past": False,

    "retries": 5,

    "retry_delay": timedelta(seconds=15)

}


def generate_metrics():

    print("Generating metrics")

    time.sleep(5)

    print("Done")


def unstable_task():

    probability = random.random()

    print(
        f"Probability={probability}"
    )

    if probability < 0.7:

        raise Exception(
            "Artificial failure"
        )

    print("Success")


def check_clickhouse():

    client = Client(

        host="clickhouse",

        database="analytics",

        user="admin",

        password="admin123"

    )

    count = client.execute(

        """
        SELECT count()
        FROM events
        """

    )[0][0]

    print(
        f"Rows={count}"
    )


with DAG(

    dag_id="ml_pipeline",

    start_date=datetime(
        2025,
        1,
        1
    ),

    catchup=False,

    schedule="* * * * *",

    default_args=default_args

) as dag:

    generate = PythonOperator(

        task_id="generate",

        python_callable=generate_metrics

    )

    unstable = PythonOperator(

        task_id="unstable",

        python_callable=unstable_task

    )

    clickhouse = PythonOperator(

        task_id="check_clickhouse",

        python_callable=check_clickhouse

    )

    (
        generate
        >>
        unstable
        >>
        clickhouse
    )
