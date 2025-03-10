

from fastapi import APIRouter, BackgroundTasks

from schemas.payments import PaymentIn, PaymentOut
from controller.payments import PaymentController
from utils.sql import check_created_by_admin

payment_router = APIRouter()

@payment_router.post("/payments", response_model=PaymentOut)
def make_payment(data: PaymentIn, bg_task: BackgroundTasks):
    check_created_by_admin(data.created_by_id)
    return PaymentController.create_payment(data.__dict__, bg_task)


@payment_router.get("/payments/{payment_id}", response_model=PaymentOut)
def get_payment(payment_id: int, created_by_id: int):
    check_created_by_admin(created_by_id)
    return PaymentController.get_payment(payment_id)


@payment_router.put("/payments/{payment_id}", response_model=PaymentOut)
def update_payment(payment_id: int, data: PaymentIn):
    return PaymentController.update_payment(payment_id, data.__dict__)


@payment_router.delete("/payments/{payment_id}")
def delete_payment(payment_id: int,created_by_id: int):
    check_created_by_admin(created_by_id)
    return PaymentController.delete_payment(payment_id)





