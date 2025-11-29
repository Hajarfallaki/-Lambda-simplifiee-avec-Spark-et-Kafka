from pyspark.sql import SparkSession
from pyspark.sql.functions import sum as sum_

spark = SparkSession.builder.appName("batch-job").getOrCreate()

df = spark.read.json("/app/datasets/transactions.json")

agg = df.groupBy("customer").agg(sum_("amount").alias("total_amount"))

agg.show()

# Écrire en une seule partition (un seul part-00000-*.json)
agg.coalesce(1).write.mode("overwrite").json("/app/serving_view_temp")

spark.stop()
