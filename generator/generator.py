from clickhouse_driver import Client

import random
import time

from datetime import datetime


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

    noise = random.gauss(0, 5)

    target = (
        2.0 * feature1
        + 0.5 * feature2
        + noise
    )

    row = [

        (
            datetime.now(),
            random.randint(1, 1000),
            feature1,
            feature2,
            target
        )

    ]

    client.execute(
        """
        INSERT INTO events
        VALUES
        """,
        row
    )

    print("Inserted", row)

    time.sleep(1)
