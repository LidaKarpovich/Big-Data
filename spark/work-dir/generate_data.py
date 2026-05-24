from pyspark.sql import SparkSession
from pyspark.sql.functions import rand,col

spark=SparkSession.builder \
    .appName("GenerateData") \
    .getOrCreate()

df=spark.range(0,3000000)

df=df \
.withColumn("x1",rand()) \
.withColumn("x2",rand()) \
.withColumn("x3",rand())

df=df.withColumn(
    "label",
    (col("x1")+col("x2")>1).cast("int")
)

df=df.repartition(12)

df.write.mode("overwrite").parquet("/opt/airflow/data/ml_input")

spark.stop()
