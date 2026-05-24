from clickhouse_driver import Client

client=Client(
    host="clickhouse",
    database="analytics",
    user="admin",
    password="admin123"
)

count=client.execute(
"""
SELECT count()
FROM ml_results
"""
)[0][0]

if count==0:
    raise Exception(
        "No results"
    )

print(
f"Rows={count}"
)
