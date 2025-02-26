from kafka import KafkaProducer, KafkaConsumer
import json




from tools.log import Log
from config.setting import settings



class KafkaCustomProducer:
    @staticmethod
    def connect_kafka()-> KafkaProducer:
        bootstrap_servers = settings.KAFKA_BOOTSTRAP_SERVERS.split(',')
        producer = KafkaProducer(
                                bootstrap_servers=bootstrap_servers,
                                security_protocol="SASL_PLAINTEXT",
                                sasl_mechanism="SCARM-SHA-256",
                                sasl_plain_username=settings.KAFKA_USERNAME,
                                sasl_plain_password=settings.KAFKA_PASSWORD,
                                value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                                reties=3,
                                retry_backoff_ms=1000,
                                acks=1
                                )
        if not producer.bootstrap_connected():
            Log.error(f"{KafkaProducer.connect_kafka.__name__} - Unable to connect to Kafka")
            raise Exception("Unable to connect to Kafka")
        return producer
    



class KafkaCustomConsumer:
    @staticmethod
    def connect_kafka()-> KafkaConsumer:
        bootstrap_servers = settings.KAFKA_BOOTSTRAP_SERVERS.split(',')
        consumer = KafkaConsumer(
                                settings.KAFKA_TOPIC,
                                bootstrap_servers=bootstrap_servers,
                                security_protocol="SASL_PLAINTEXT",
                                sasl_mechanism="SCARM-SHA-256",
                                sasl_plain_username=settings.KAFKA_USERNAME,
                                sasl_plain_password=settings.KAFKA_PASSWORD,
                                value_deserializer=lambda v: json.loads(v.decode('utf-8')),
                                auto_offset_reset='auto_offset',
                                enable_auto_commit=True,
                                )
        if not consumer.bootstrap_connected():
            Log.error(f"{KafkaConsumer.connect_kafka.__name__} - Unable to connect to Kafka")
            raise Exception("Unable to connect to Kafka, make sure the topic exists")
        return consumer
