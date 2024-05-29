import json
from kafka import KafkaProducer

class KafkaManager:
    def __init__(self, bootstrap_servers='localhost:9092'):
        self.bootstrap_servers = bootstrap_servers

    def create_producer(self, topic):
        """Creates and returns a Kafka producer for the specified topic."""
        return KafkaProducer(
            bootstrap_servers=self.bootstrap_servers,
            value_serializer=lambda m: json.dumps(m).encode('ascii')
        )

# Example usage (you can put this in a separate main.py or use it directly):
if __name__ == "__main__":
    kafka_manager = KafkaManager()
    producer = kafka_manager.create_producer(topic='alain_news')
    sample_article = {"title": "Test Article", "content": "Some content..."}
    producer.send('alain_news', sample_article)
    producer.flush()