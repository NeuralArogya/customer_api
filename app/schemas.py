from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

# --- Order Schemas ---
class OrderOut(BaseModel):
    orderNumber: int
    orderDate: datetime
    requiredDate: datetime
    shippedDate: Optional[datetime] = None
    status: str
    comments: Optional[str] = None
    customerNumber: int

    class Config:
        from_attributes = True


# --- Payment Schemas ---
class PaymentOut(BaseModel):
    customerNumber: int
    checkNumber: str
    paymentDate: datetime
    amount: float

    class Config:
        from_attributes = True


# --- Customer Schemas ---
class CustomerCreate(BaseModel):
    customerNumber: int
    customerName: str
    contactLastName: str
    contactFirstName: str
    phone: str
    addressLine1: str
    addressLine2: Optional[str] = None
    city: str
    state: Optional[str] = None
    postalCode: Optional[str] = None
    country: str
    salesRepEmployeeNumber: Optional[int] = None
    creditLimit: Optional[float] = None


class CustomerUpdate(BaseModel):
    customerName: Optional[str] = None
    contactLastName: Optional[str] = None
    contactFirstName: Optional[str] = None
    phone: Optional[str] = None
    addressLine1: Optional[str] = None
    addressLine2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postalCode: Optional[str] = None
    country: Optional[str] = None
    salesRepEmployeeNumber: Optional[int] = None
    creditLimit: Optional[float] = None


class CustomerOut(BaseModel):
    customerNumber: int
    customerName: str
    contactLastName: str
    contactFirstName: str
    phone: str
    addressLine1: str
    addressLine2: Optional[str] = None
    city: str
    state: Optional[str] = None
    postalCode: Optional[str] = None
    country: str
    salesRepEmployeeNumber: Optional[int] = None
    creditLimit: Optional[float] = None
    orders: List[OrderOut] = []
    payments: List[PaymentOut] = []

    class Config:
        from_attributes = True