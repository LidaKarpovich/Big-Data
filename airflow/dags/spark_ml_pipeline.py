from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    "retries": 3,
    "retry_delay": timedelta(seconds=30),
}

with DAG(
    dag_id="spark_ml_pipeline",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    default_args=default_args,
):
    generate = BashOperator(
        task_id="generate_data",
        bash_command="""
docker exec spark-master \
/opt/spark/bin/spark-submit \
--master spark://spark-master:7077 \
/opt/spark/work-dir/generate_data.py
"""
    )
    ml = BashOperator(
        task_id="distributed_ml",
        bash_command="""
docker exec spark-master \
/opt/spark/bin/spark-submit \
--master spark://spark-master:7077 \
/opt/spark/work-dir/distributed_ml.py
"""
    )
    clickhouse = BashOperator(
        task_id="write_clickhouse",
        bash_command="""
docker exec spark-master \
/opt/spark/bin/spark-submit \
--master spark://spark-master:7077 \
/opt/spark/work-dir/write_clickhouse.py
"""
    )
    validate = BashOperator(
        task_id="validate",
        bash_command="""
echo Pipeline finished
"""
    )
    generate >> ml >> clickhouse >> validate