
from utils import sql
from models.transactions import Transaction


class TransactionsController:

    @staticmethod
    def save_transaction(transaction) -> None:
        """	consume transactions from kafka and save to the database


        Args:
            transaction (Transaction): transaction object
        
        Returns:
            None
        """	
        transaction = Transaction(**transaction)
        sql.add_object_to_database(Transaction, transaction)
        