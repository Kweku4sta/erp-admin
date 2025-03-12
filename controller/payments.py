from concurrent.futures import ThreadPoolExecutor

from schemas.payments import PaymentIn, PaymentUpdate, PaymentUpdateFields
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
        bg_task.add_task(KafkaStreamProducer.send_json_data_to_topic, "payments", payment.json_data())
        PaymentController.executor.submit(AuditLogger.log_activity, payment.created_by_id, f"Created the payment with ID:{payment.id}", "CREATE")
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
                
                payment_data = {key: value for key, value in payment_data.items() if value is not None}
                for key, value in payment_data.items():
                    setattr(payment, key, value)
                db_session.commit()
                db_session.refresh(payment)
                PaymentController.executor.submit(AuditLogger.log_activity, payment.created_by_id, f"Updated the payment with ID:{payment.id}", "UPDATE")
                return payment.json_data()
            raise HTTPException(status_code=404, detail="Payment not found")


    @staticmethod
    def delete_payment(payment_id: int, created_by_id: int) -> dict:
        """Delete Payment
        This method deletes a payment

        Args:
            payment_id (int): [description]
            created_by_id (int): the user deleting the payment

        Returns:
            dict: [description]
        """
        with session.CreateDBSession() as db_session:
            payment = db_session.get(Payment, payment_id)
            if payment:
                if payment.is_reversed:
                    raise HTTPException(status_code=400, detail="Payment is reversed")
                db_session.delete(payment)
                db_session.commit()
                PaymentController.executor.submit(AuditLogger.log_activity, created_by_id, f"Deleted the payment with id:{payment.id}", "DELETE")
                return payment.json_data()
            raise HTTPException(status_code=404, detail="Payment not found")
        

    @staticmethod
    def reverse_payment(payment_id: int, created_by_id: int) -> dict:
        """Reverse Payment
        This method reverses a payment

        Args:
            payment_id (int): [description]
            created_by_id (int): the user reversing the payment

        Returns:
            dict: [description]
        """
        with session.CreateDBSession() as db_session:
            payment = db_session.get(Payment, payment_id)
            if payment:
                if payment.is_reversed:
                    raise HTTPException(status_code=400, detail="Payment is already reversed")
                payment.is_reversed = True
                db_session.commit()
                PaymentController.executor.submit(AuditLogger.log_activity, created_by_id, f"Reversed the payment with ID:{payment.id}", "UPDATE")
                return payment.json_data()
            raise HTTPException(status_code=404, detail="Payment not found")