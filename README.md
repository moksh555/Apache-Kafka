# 📡 Apache Kafka — Real-Time News Streaming Pipeline

A Python-based streaming data pipeline that fetches live business news headlines and processes them through **Apache Kafka** using **Apache Spark Structured Streaming** and **spaCy NLP**. The pipeline demonstrates a producer–consumer architecture with Named Entity Recognition (NER) applied to live data.

## ✨ Features

- **Live news ingestion** — polls the NewsAPI every 60 seconds for top US business headlines and publishes article content to a Kafka topic (`ptopic`)
- **Spark Structured Streaming consumer** — reads the Kafka topic as a streaming DataFrame in real time
- **spaCy NER extraction** — a PySpark UDF applies `en_core_web_sm` to extract named entities (people, organizations, locations) from each article
- **Word/entity frequency aggregation** — groups and counts extracted entities, maintaining a live top-10 ranking per micro-batch
- **Downstream Kafka producer** — publishes the top-10 entity frequency dictionary to a second topic (`ctopic`) for downstream consumption

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| Language | Python 3 |
| Message Broker | Apache Kafka |
| Stream Processing | Apache Spark Structured Streaming (PySpark) |
| NLP | spaCy (`en_core_web_sm`) |
| Data Source | NewsAPI (`newsapi-python`) |
| Serialization | UTF-8 strings / JSON |

## 🚀 Setup & Installation

**Prerequisites:** Python 3.8+, Apache Kafka running on `localhost:9092`, Apache Spark

```bash
# 1. Clone the repository
git clone https://github.com/moksh555/Apache-Kafka.git
cd Apache-Kafka

# 2. Install Python dependencies
pip install kafka-python newsapi-python pyspark spacy

# 3. Download the spaCy language model
python -m spacy download en_core_web_sm

# 4. Start Kafka and create the required topics
kafka-topics.sh --create --topic ptopic --bootstrap-server localhost:9092
kafka-topics.sh --create --topic ctopic --bootstrap-server localhost:9092
```

## ▶️ Usage

Run each script in a separate terminal:

```bash
# Terminal 1 — Start the news producer (polls every 60 seconds)
python main.py

# Terminal 2 — Start the Spark Streaming consumer/NER processor
spark-submit main2.py
```

## 🏗️ Architecture

```
NewsAPI ──► main.py (KafkaProducer) ──► [ptopic] ──► main2.py (Spark Streaming)
                                                           │
                                                    spaCy NER UDF
                                                           │
                                                  Entity frequency count
                                                           │
                                             [ctopic] ◄── KafkaProducer
```

`main.py` acts as a **producer**: it calls NewsAPI, iterates over articles, and sends each article's content as a UTF-8 string to the `ptopic` Kafka topic. `main2.py` acts as a **Spark Streaming consumer**: it reads from `ptopic`, applies a spaCy UDF to extract named entities, aggregates entity counts per micro-batch, and publishes the top-10 results back to `ctopic`.
