import json
import hashlib
from datetime import datetime

from tenacity import retry, stop_after_attempt, wait_fixed
from fastapi import Request
from kafka import KafkaProducer, KafkaConsumer, errors


from tools.log import Log
from services.kafka import KafkaCustomProducer, KafkaCustomConsumer 

_loggers = Log(name=f"{__name__}")


def on_stream_stream(data):
    _loggers.info(f"KAFKA:data published successfully to kafka topic: {data.topic()}")

def on_stream_error(exc):
    _loggers.error(f"KAFKA:error while publishing data to kafka: {exc}", exc_info=True)
    raise exc


class KafkaStreamProducer:
    @classmethod
    def __connect_to_kafka(cls)->KafkaProducer:
        return KafkaCustomProducer.connect_kafka()
    

    @classmethod
    @retry(stop=stop_after_attempt(5))
    def send_json_data_to_topic(cls, topic: str, data: dict, request_details: Request = None)-> None:
        try:
            producer = cls.__connect_to_kafka()
            producer.send(topic, value=data).add_callback(on_stream_stream).add_errback(on_stream_error)
            producer.flush()
        # except kafka errors 
        except Exception as e:
            _loggers.error(f"{cls.send_json_data_to_topic.__name__} - {str(e.args[0])}")
            raise Exception("Unable to connect to Kafka") from e
        finally:
            producer.close()


    @classmethod
    def send_kafka_log_entry(cls, log_entry: dict)-> None:
        log_entry["created_at"] = datetime.utcnow().isoformat()
        log_entry["service"] = "ADMIN PORTAL"
        log_entry_id  = hashlib.sha256(json.dumps(log_entry).encode("utf-8")).hexdigest()
        log_entry["id"] = log_entry_id
        cls.send_json_data_to_topic("audit_logs", log_entry)



class KafkaStreamConsumer:
    @classmethod
    def __connect_to_kafka(cls)->KafkaConsumer:
        return KafkaCustomConsumer.connect_kafka()
    

    @classmethod
    @retry(stop=stop_after_attempt(5), wait=wait_fixed(2))
    def consume_json_data_from_topic(cls, topic: str)-> dict:
        try:
            consumer = cls.__connect_to_kafka()
            for message in consumer:
                return message.value
        except errors.NoBrokersAvailable:
            _loggers.error(f"{cls.consume_json_data_from_topic.__name__} - No brokers available")
            raise Exception("Unable to connect to Kafka, make sure the topic exists")
        finally:
            consumer.close()



    
    



