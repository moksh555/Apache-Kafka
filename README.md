# Apache-Kafka

# Kafka Streamer with NLP Processing
This project demonstrates a real-time data pipeline using Apache Kafka, Kibana, and Elasticsearch. The pipeline involves fetching news articles, streaming them through Kafka, and applying Natural Language Processing (NLP) using SpaCy to extract and analyze entities from the news content.

# Features
  News Fetching: The first script fetches top business headlines from the US using the News API and sends the content to a Kafka topic.
  Stream Processing: The second script reads the news data from the Kafka topic, processes it using SpaCy to perform Named Entity   Recognition (NER), and counts the occurrences of each entity.
  Data Visualization: Data can be visualized using Kibana, with Elasticsearch storing the processed data.

# Project Structure
  main.py: Fetches news articles and pushes them to a Kafka topic.
  main2.py: Consumes news data from Kafka, applies NLP for entity extraction, and counts the occurrences of each entity.

# Tools and Technologies
  Kafka: Used for streaming data between producers and consumers.
  Apache Spark: Utilized for processing streaming data in real-time.
  SpaCy: A library for advanced NLP tasks like Named Entity Recognition (NER).
  Kibana & Elasticsearch: Used for data storage and visualization.
  Python: The primary programming language for writing the scripts.

# Setup and Usage
  Kafka Setup: Ensure you have Kafka running locally or on a server.
  News API: Obtain an API key from NewsAPI and replace it in main.rtf.
  Run the Producer: Use the first script in my case(main.py) to fetch and push news data to the Kafka topic.
  Run the Consumer: Use the second script to process the streamed data and send the processed output to a Kafka topic for visualization.
  Kibana & Elasticsearch: Configure Kibana and Elasticsearch to visualize the processed data.
  
# Future Enhancements
  Integrate additional data sources.
  Improve entity extraction accuracy with custom SpaCy models.
  Enhance the data pipeline to handle larger datasets and different content categories.
