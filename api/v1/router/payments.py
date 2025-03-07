

from fastapi import APIRouter, BackgroundTasks

from schemas.payments import PaymentIn, PaymentOut
from controller.payments import PaymentController

payment_router = APIRouter()

@payment_router.post("/payments", response_model=PaymentOut)
def make_payment(data: PaymentIn, bg_task: BackgroundTasks):
    return PaymentController.create_payment(data.__dict__, bg_task)


