from pyspark.sql import SparkSession
from pyspark.sql.functions import rand

spark = (
    SparkSession.builder
    .appName("GenerateData")
    .getOrCreate()
)

N = 5_000_000

df = (
    spark.range(N)
    .withColumn("x1", rand())
    .withColumn("x2", rand())
    .withColumn("label",
        (rand() > 0.5).cast("integer")
    )
)

df.write.mode("overwrite").parquet(
    "/opt/spark-data/raw/train"
)

print(df.count())

spark.stop()
