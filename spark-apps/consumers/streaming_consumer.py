from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("HeartRateStreaming") \
    .master("spark://spark-master:7077") \
    .getOrCreate()

df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka1:9092") \
    .option("subscribe", "heart-rate-data") \
    .load()

df.printSchema()

df.show()

df.writeStream \
    .format("console") \
    .start() \
    .awaitTermination()

spark.stop()