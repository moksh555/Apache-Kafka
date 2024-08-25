from pyspark.sql import SparkSession
from pyspark.sql.functions import col, explode
from pyspark.sql.types import ArrayType, StringType
from pyspark.sql.functions import udf
from kafka import KafkaProducer
import spacy 
import json

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

spark = SparkSession.builder \
    .appName("KafkaStreamingExample") \
    .getOrCreate()

kafka_bootstrap_servers = "localhost:9092"
kafka_topic = "ptopic"

raw_stream_df = spark.readStream\
                .format("kafka")\
                .option("kafka.bootstrap.servers", kafka_bootstrap_servers)\
                .option("subscribe", kafka_topic)\
                .load()

parsed_stream_df = raw_stream_df \
    .selectExpr("CAST(value AS STRING) as data")

nlp = spacy.load("en_core_web_sm")

@udf(ArrayType(StringType()))
def spacy_ner_and_extract_words(text):
    lines = nlp(text)
    return [words.text for words in lines.ents]


# Register the UDF
spark.udf.register("spacy_ner_and_extract_words", spacy_ner_and_extract_words)

# Apply the function to the streaming DataFrame
word_count_df = parsed_stream_df \
    .select("data", explode(spacy_ner_and_extract_words("data")).alias("word")) \
    .groupBy("word") \
    .count() \
    .orderBy(col("count").desc())

# Define a function to show the word count
def process_word_count(df,epoch_id):
    #df.show(truncate=False)
    word_count_dict = dict(df.take(10))  # Assuming df has "word" and "count" columns
    producer.send('ctopic', value=word_count_dict)
    print("-------------------------------------------------------------------------")
    print(word_count_dict)
    print("-------------------------------------------------------------------------")
    
# Apply the function to the streaming DataFrame
query = word_count_df.writeStream \
    .outputMode("complete") \
    .foreachBatch(process_word_count) \
    .start()

query.awaitTermination()
