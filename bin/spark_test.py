# - read from any kafka
# - do computation
# - write back to kafka

from kafka import KafkaProducer
from pyspark import SparkContext
from pyspark.sql import SparkSession, Row
from pyspark.sql.functions import explode, window
from pyspark.sql.functions import split, decode, udf
from pyspark.sql.types import StringType
from pyspark.streaming import StreamingContext
# from pyspark.sql.functions import aggregate, explode, window
# from pyspark.sql.functions import split, decode, udf
# from pyspark.sql.types import StringType
# from pyspark.streaming import StreamingContext

import atexit
import json
import logging
import sys
import time

logger_format = '%(asctime)-15s %(message)s'
logging.basicConfig(format=logger_format)
logger = logging.getLogger('stream-processing')
logger.setLevel(logging.INFO)

topic = None
target_topic = None
brokers = None
kafka_producer = None


if __name__ == "__main__":
    spark = SparkSession.builder.appName('spark_streaming').getOrCreate()

    spark.sparkContext.setLogLevel("WARN")
    scope_name = "my-scope"
    stream_name = "my-stream"
    controller_url = "tcp://localhost:9090"

    df = spark \
            .readStream \
            .format("pravega") \
            .option("controller", controller_url) \
            .option("scope", scope_name) \
            .option("stream", stream_name) \
            .option("start_stream_cut", "earliest") \
            .load()

    print(">>>" * 100)
    print(df)
    print(">>>" * 100)
    words = df.withColumn('value', decode(df.event, 'UTF-8'))
    print(">>>2" * 100)
    print(words.value)
    print(">>>" * 100)

    query = words \
        .writeStream \
        .outputMode("append") \
        .format("console") \
        .start()

    query.awaitTermination()
    exit()
