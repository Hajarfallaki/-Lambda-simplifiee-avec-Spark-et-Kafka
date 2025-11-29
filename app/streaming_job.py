from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, sum as sum_
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

spark = SparkSession.builder.appName("streaming-job").getOrCreate()

schema = StructType([
    StructField("customer", StringType()),
    StructField("amount", IntegerType())
])

stream_df = (
    spark.readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", "broker:9092")
    .option("subscribe", "real-time-orders")
    .load()
)

json_df = stream_df.select(from_json(col("value").cast("string"), schema).alias("data")) \
    .select("data.*")

agg = json_df.groupBy("customer").agg(sum_("amount").alias("total_amount"))

query = (
    agg.writeStream
    .outputMode("complete")
    .format("console")
    .option("truncate", "false")
    .start()
)

query.awaitTermination()