from typing import Dict, Union
from concurrent.futures import ThreadPoolExecutor




from services.stream import KafkaStreamProducer
from utils import sql
from models.admins import Admin

class AuditLogger:
    executor = ThreadPoolExecutor(max_workers=10)
    @staticmethod
    def log_activity( issuer: Union[str, int], description:str, method:str) -> None:
        if isinstance(issuer, int):
            user = sql.get_object_by_id_from_database(Admin, issuer)
            issuer = user.full_name
        log_entry = {
            "issuer": issuer,
            "description": description,
            "method": method
        }
        AuditLogger.executor.submit(KafkaStreamProducer.send_kafka_log_entry, log_entry)