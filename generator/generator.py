from clickhouse_driver import Client
import random
import time

def connect():
    while True:
        try:
            client = Client(
                host="clickhouse",
                database="analytics",
                user="admin",
                password="admin123"
            )
            client.execute("SELECT 1")
            print("Connected")
            return client
        except Exception as e:
            print("Waiting ClickHouse", e)
            time.sleep(5)

client = connect()

while True:
    feature1 = random.uniform(0, 100)
    feature2 = random.uniform(0, 50)
    feature3 = random.uniform(0, 30)
    label = 1.0 if (feature1 + feature2 > 75) else 0.0

    row = [(
        random.randint(1, 1000),
        float(feature1),
        float(feature2),
        float(feature3),
        label
    )]

    client.execute(
        "INSERT INTO analytics.events (id, x1, x2, x3, label) VALUES",
        row
    )
    print("Inserted", row)
    time.sleep(1)