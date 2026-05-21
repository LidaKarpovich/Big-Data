from pyspark.sql import SparkSession

from pyspark.ml.feature import VectorAssembler

from pyspark.ml.classification import LogisticRegression

from pyspark.ml import Pipeline

spark = (
    SparkSession.builder
    .appName("DistributedML")
    .getOrCreate()
)

spark.sparkContext.setCheckpointDir(
    "/opt/spark-data/checkpoints"
)

df = spark.read.parquet(
    "/opt/spark-data/raw/train"
)

print(
    "Partitions:",
    df.rdd.getNumPartitions()
)

assembler = VectorAssembler(
    inputCols=["x1","x2"],
    outputCol="features"
)

lr = LogisticRegression(
    featuresCol="features",
    labelCol="label",
    maxIter=20
)

pipeline = Pipeline(
    stages=[
        assembler,
        lr
    ]
)

model = pipeline.fit(df)

pred = model.transform(df)

(
    pred
    .select(
        "id",
        "prediction"
    )
    .write
    .mode("overwrite")
    .parquet(
        "/opt/spark-data/output/predictions"
    )
)

print(
    pred.count()
)

spark.stop()
