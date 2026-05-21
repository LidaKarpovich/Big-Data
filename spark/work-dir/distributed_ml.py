from pyspark.sql import SparkSession
from pyspark.sql.functions import rand, col
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.classification import LogisticRegression

# 1. Spark session
spark = SparkSession.builder \
    .appName("FaultToleranceDemo") \
    .getOrCreate()

print("Spark started")

# 2. Create large synthetic dataset (IMPORTANT: parallelism)
df = spark.range(0, 5_000_000) \
    .withColumn("x1", rand()) \
    .withColumn("x2", rand()) \
    .withColumn("x3", rand())

# binary label
df = df.withColumn("label", (col("x1") + col("x2") > 1).cast("int"))

print("Dataset created")

# 3. Force distributed processing (key point for demo)
df = df.repartition(8)

# 4. Feature vector
assembler = VectorAssembler(
    inputCols=["x1", "x2", "x3"],
    outputCol="features"
)

df = assembler.transform(df).select("features", "label")

# 5. Split
train, test = df.randomSplit([0.8, 0.2], seed=42)

# 6. Model
lr = LogisticRegression(maxIter=10)

model = lr.fit(train)

print("Model trained")

# 7. Evaluation
pred = model.transform(test)
pred.select("prediction", "label").show(10)

print("DONE")
spark.stop()
