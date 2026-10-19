import json
import os
from pathlib import Path
from kafka import KafkaProducer
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent / '.env')

KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS')
KAFKA_TOPIC = os.getenv('KAFKA_TOPIC')

if not KAFKA_BOOTSTRAP_SERVERS or not KAFKA_TOPIC:
    raise RuntimeError(
        "KAFKA_BOOTSTRAP_SERVERS и KAFKA_TOPIC должны быть заданы в .env"
    )

_producer: KafkaProducer | None = None


def get_producer() -> KafkaProducer:
    global _producer
    if _producer is None:
        _producer = KafkaProducer(
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS.split(','),
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            acks='all',
            retries=3,
            linger_ms=10,
        )
    return _producer


def close_producer():
    if _producer is not None:
        _producer.close()
