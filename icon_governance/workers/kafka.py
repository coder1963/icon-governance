from time import sleep
from typing import Any

from confluent_kafka import DeserializingConsumer, KafkaError
from confluent_kafka.admin import AdminClient
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.protobuf import ProtobufDeserializer
from confluent_kafka.serialization import StringDeserializer

from pydantic import BaseModel, validator

from loguru import logger
# from icon_governance.log import logger
from icon_governance.config import settings
from icon_governance.schemas.transaction_raw_pb2 import TransactionRaw


class KafkaClient(BaseModel):
    name: str = None
    schema_registry_url: str = settings.SCHEMA_REGISTRY_URL
    schema_registry_client: Any = None
    sleep_seconds: float = 0.25

    session: Any = None

    kafka_server: str = settings.KAFKA_BROKER_URL
    consumer_group: str

    topic: str

    consumer: Any = None
    consumer_schema: Any = None
    consumer_deserializer: Any = None

    def __init__(self, **data: Any):
        super().__init__(**data)
        if self.name is None:
            self.name = self.topic

        self.consumer_deserializer = ProtobufDeserializer(TransactionRaw)

        self.consumer = DeserializingConsumer(
            {
                "bootstrap.servers": self.kafka_server,
                "group.id": self.consumer_group,
                "key.deserializer": StringDeserializer("utf_8"),
                "value.deserializer": self.consumer_deserializer,
                "auto.offset.reset": "earliest",
            }
        )

        admin_client = AdminClient({'bootstrap.servers': self.kafka_server})
        topics = admin_client.list_topics().topics

        if self.topic not in topics:
            raise RuntimeError()

        self.init()

    def start(self):
        self.consumer.subscribe([self.topic])
        logger.info("Kafka consumer connected...")

        while True:
            # Poll for a message
            msg = self.consumer.poll(timeout=1)

            # If no new message, try again
            if msg is None:
                continue

            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    err_msg = (
                        "{topic} {partition} reached end at offset {offset}".format(
                            topic=msg.topic(),
                            partition=msg.partition(),
                            offset=msg.offset(),
                        )
                    )
                    logger.error("Kafka consumer: " + err_msg)
                if msg.error().code() == KafkaError.UNKNOWN_TOPIC_OR_PART:
                    logger.error(f"Kafka consumer: Kafka topic {msg.topic()} not ready. Restarting.")
                elif msg.error():
                    logger.error("Kafka consumer: " + str(msg.error()))
                sleep(1)
                continue
            else:
                self.process(msg)

    def init(self):
        """Overridable process that runs on init."""
        pass

    def process(self, msg):
        """Overridable process that processes each message."""
        pass
