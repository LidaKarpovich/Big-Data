from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .appName("ClickHouseWriter")
    .getOrCreate()
)

df = spark.read.parquet(
    "/opt/spark-data/output/predictions"
)

(
    df.write
    .format("jdbc")
    .option(
        "url",
        "jdbc:clickhouse://clickhouse:8123/analytics"
    )
    .option(
        "dbtable",
        "predictions"
    )
    .option(
        "user",
        "admin"
    )
    .option(
        "password",
        "admin123"
    )
    .mode("append")
    .save()
)

spark.stop()
