from pyspark.sql import SparkSession
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.evaluation import BinaryClassificationEvaluator


spark = SparkSession.builder \
    .appName("DistributedML") \
    .getOrCreate()

df = spark.read.parquet("/opt/airflow/data/ml_input")

assembler = VectorAssembler(
    inputCols=["x1", "x2", "x3"],
    outputCol="features"
)
df = assembler.transform(df)

train, test = df.randomSplit([0.8, 0.2], seed=42)

lr = LogisticRegression(maxIter=10)
model = lr.fit(train)
pred = model.transform(test)

evaluator = BinaryClassificationEvaluator(
    labelCol="label",
    rawPredictionCol="rawPrediction",
    metricName="areaUnderROC"
)
metric = evaluator.evaluate(pred)
rows = df.count()

spark.createDataFrame(
    [(float(metric), int(rows))],
    ["metric", "rows_processed"]
).write.mode("overwrite").parquet("/opt/airflow/data/ml_result")

spark.stop()
