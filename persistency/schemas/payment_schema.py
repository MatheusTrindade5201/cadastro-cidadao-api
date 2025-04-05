from datetime import date
from typing import Optional

from pydantic import BaseModel


class PaymentRegistry(BaseModel):
    order_id: str
    payment_id: str
    status: str
    payment_method: str
    value: int
    email: str


class PaymentOutput(BaseModel):
    email: str
    value: int
    status: str

    class Config:
        orm_mode = True


class ExportPaymentsCSV(BaseModel):
    email: Optional[str]
    initial_date: Optional[date]
    final_date: Optional[date]


class OutputPaymentCSV(BaseModel):
    id: int
    email: str
    payment_method: str
    order_id: str
    value: int
    payment_id: str
    status: str
    datetime: date
