from pyspark.sql import SparkSession
from pyspark.sql.functions import col, rand
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.classification import LogisticRegression
from pyspark.ml import Pipeline


def main():
    spark = (
        SparkSession.builder
        .appName("Distributed-ML-Demo")
        .getOrCreate()
    )

    print("Spark session started")

    # 1. Генерируем БОЛЬШОЙ распределённый датасет
    # важно: range = уже distributed dataset
    df = spark.range(0, 5_000_000).toDF("id")

    df = (
        df.withColumn("f1", rand())
          .withColumn("f2", rand())
          .withColumn("f3", rand())
          .withColumn("label", (col("f1") + col("f2") > 1).cast("int"))
    )

    # 2. Принудительно распараллеливаем (ВАЖНО для демонстрации workers)
    df = df.repartition(8)

    print("Partitions:", df.rdd.getNumPartitions())

    # 3. Feature engineering
    assembler = VectorAssembler(
        inputCols=["f1", "f2", "f3"],
        outputCol="features"
    )

    # 4. ML model
    lr = LogisticRegression(
        featuresCol="features",
        labelCol="label",
        maxIter=10
    )

    pipeline = Pipeline(stages=[assembler, lr])

    # 5. train/test split (тоже distributed)
    train, test = df.randomSplit([0.8, 0.2], seed=42)

    print("Training started...")

    model = pipeline.fit(train)

    print("Training finished")

    # 6. evaluation (distributed inference)
    predictions = model.transform(test)

    predictions.select("label", "prediction").show(20)

    accuracy = predictions.filter(
        col("label") == col("prediction")
    ).count() / test.count()

    print(f"Accuracy: {accuracy}")

    # 7. forcing execution (important for Spark lazy eval)
    predictions.count()

    spark.stop()


if __name__ == "__main__":
    main()
