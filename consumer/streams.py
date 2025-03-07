from json import loads
from typing import Any


from models.transactions import Transaction
from controller.transactions import TransactionsController
from services.kafka import KafkaCustomConsumer



def callback_for_saving_transaction(transaction: dict[str, Any]):
    traction_payload = loads(transaction)
    transaction = Transaction(**traction_payload)
    TransactionsController.save_transaction(transaction)
    return transaction.json_data()


def save_transaction():
    print("Saving transaction from backend server")
    kafka_instance = KafkaCustomConsumer(
        topic="transactions",
        callback=callback_for_saving_transaction
    )
    kafka_instance.co