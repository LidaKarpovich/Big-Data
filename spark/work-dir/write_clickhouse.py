import pandas as pd
from clickhouse_driver import Client
from datetime import datetime

client = Client(
    host="clickhouse",
    database="analytics",
    user="admin",
    password="admin123"
)

df = pd.read_parquet("/opt/airflow/data/ml_result")

client.execute(
    """
    INSERT INTO ml_results (ts, accuracy, rows_processed) VALUES
    """,
    [(
        datetime.now(),
        float(df.metric.iloc[0]),
        int(df.rows_processed.iloc[0])
    )]
)
print("Inserted", df.metric.iloc[0])