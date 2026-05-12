from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
import logging

logger = logging.getLogger(__name__)

class Customer(Base):
    __tablename__ = "customers"

    customerNumber = Column(Integer, primary_key=True, index=True)
    customerName = Column(String(50), nullable=False)
    contactLastName = Column(String(50), nullable=False)
    contactFirstName = Column(String(50), nullable=False)
    phone = Column(String(50), nullable=False)
    addressLine1 = Column(String(50), nullable=False)
    addressLine2 = Column(String(50), nullable=True)
    city = Column(String(50), nullable=False)
    state = Column(String(50), nullable=True)
    postalCode = Column(String(15), nullable=True)
    country = Column(String(50), nullable=False)
    salesRepEmployeeNumber = Column(Integer, nullable=True)
    creditLimit = Column(Float, nullable=True)

    orders = relationship("Order", back_populates="customer")
    payments = relationship("Payment", back_populates="customer")


class Order(Base):
    __tablename__ = "orders"

    orderNumber = Column(Integer, primary_key=True, index=True)
    orderDate = Column(DateTime, nullable=False)
    requiredDate = Column(DateTime, nullable=False)
    shippedDate = Column(DateTime, nullable=True)
    status = Column(String(15), nullable=False)
    comments = Column(String, nullable=True)
    customerNumber = Column(Integer, ForeignKey("customers.customerNumber"))

    customer = relationship("Customer", back_populates="orders")


class Payment(Base):
    __tablename__ = "payments"

    customerNumber = Column(Integer, ForeignKey("customers.customerNumber"), primary_key=True)
    checkNumber = Column(String(50), primary_key=True)
    paymentDate = Column(DateTime, nullable=False)
    amount = Column(Float, nullable=False)

    customer = relationship("Customer", back_populates="payments")