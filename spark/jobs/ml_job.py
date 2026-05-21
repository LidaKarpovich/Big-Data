from pyspark.sql import SparkSession
from pyspark.sql.functions import rand, col
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.feature import VectorAssembler

import time


spark = SparkSession.builder \
    .appName("distributed-ml-demo") \
    .getOrCreate()


print("=== Generating distributed dataset ===")

# искусственный большой датасет (распределённый)
df = spark.range(0, 5_000_000).withColumn("x1", rand()) \
                             .withColumn("x2", rand()) \
                             .withColumn("label", (col("x1") + col("x2") > 1).cast("int"))

df = df.repartition(8)   # <-- КЛЮЧ: распределение по worker'ам

print("Partitions:", df.rdd.getNumPartitions())

assembler = VectorAssembler(inputCols=["x1", "x2"], outputCol="features")
df = assembler.transform(df).select("features", "label")

train, test = df.randomSplit([0.8, 0.2], seed=42)

print("=== Starting ML training ===")

lr = LogisticRegression(maxIter=10)

model = lr.fit(train)

print("=== Evaluating ===")

acc = model.evaluate(test).accuracy

print("Accuracy:", acc)

time.sleep(30)  # окно для убийства worker'а

print("DONE")
spark.stop()
