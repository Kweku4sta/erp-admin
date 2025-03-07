from concurrent.futures import ThreadPoolExecutor

from schemas.payments import PaymentIn
from models.payments import Payment
from utils import sql
from fastapi import HTTPException, BackgroundTasks
from services.stream import KafkaStreamProducer
from services.auditlog import AuditLogger

from utils import session


class PaymentController:
    executor = ThreadPoolExecutor(max_workers=10)
    @staticmethod
    def create_payment(payment: PaymentIn, bg_task: BackgroundTasks) -> dict:
        """Create Payment
        This method creates a payment

        Args:
            payment (PaymentIn): Payment object

        Returns:
            dict: [description]
        """
        payment = Payment(**payment)
        payment =sql.add_object_to_database(payment)
        # bg_task.add_task(KafkaStreamProducer.send_json_data_to_topic, "payments", payment.json_data())
        PaymentController.executor.submit(AuditLogger.log_activity, 1, f"Created the payment:{payment.amount}", "CREATE")
        # bg_task.add_task(KafkaStreamProducer.send_json_data_to_topic, "payments", payment.json_data())
        return payment.json_data()
    
    @staticmethod
    def get_payment(payment_id: int) -> dict:
        """Get Payment
        This method gets a payment

        Args:
            payment_id (int): [description]

        Returns:
            dict: [description]
        """
        payment = sql.get_object_by_id_from_database(Payment, payment_id)
        if payment:
            return payment.json_data()
        raise HTTPException(status_code=404, detail="Payment not found")
    

    @staticmethod
    def update_payment(payment_id: int, payment_data: dict) -> dict:
        """Update Payment
        This method updates a payment

        Args:
            payment_id (int): [description]
            payment_data (dict): [description]

        Returns:
            dict: [description]
        """
        with session.CreateDBSession() as db_session:
            payment = sql.get_object_by_id_from_database(Payment, payment_id)
            if payment:
                if payment.is_reversed:
                    raise HTTPException(status_code=400, detail="Payment is reversed")
                for key, value in payment_data.items():
                    setattr(payment, key, value)
                db_session.commit()
                return payment.json_data()
            raise HTTPException(status_code=404, detail="Payment not found")