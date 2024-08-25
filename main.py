import time
from kafka import KafkaProducer
from newsapi import NewsApiClient
import json

# Kafka configuration
kafka_bootstrap_servers = "localhost:9092"  # Replace with your Kafka bootstrap servers
kafka_topic = "ptopic"  # Replace with your Kafka input topic

# News API configuration
newsapi = NewsApiClient(api_key='3949847201814972ace05a114ae7e41f')

# Create Kafka producer
producer = KafkaProducer(
    bootstrap_servers=kafka_bootstrap_servers,value_serializer=lambda v: str(v).encode('utf-8')
)

def fetch_and_push_news():
    try:
        # Fetch top headlines from News API
        top_headlines = newsapi.get_top_headlines(country='us', category='business', language = 'en')

        # Push each article to Kafka
        for article in top_headlines['articles']:
            if (article['content']):
                producer.send(kafka_topic, value=article['content'])
        print("Kafka Got some News")

    except Exception as e:
        print(f"Error: {str(e)}")

# Schedule the job to run every 10 seconds
while True:
    fetch_and_push_news()
    time.sleep(60)
