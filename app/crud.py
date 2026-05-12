from sqlalchemy.orm import Session
from sqlalchemy import text
from app import models, schemas
import logging

logger = logging.getLogger(__name__)

# --- GET ALL CUSTOMERS ---
def get_customers(db: Session, skip: int = 0, limit: int = 100):
    logger.info(f"Fetching customers skip={skip} limit={limit}")
    return db.query(models.Customer).offset(skip).limit(limit).all()

# --- GET ONE CUSTOMER ---
def get_customer(db: Session, customer_id: int):
    logger.info(f"Fetching customer ID {customer_id}")
    customer = db.query(models.Customer).filter(
        models.Customer.customerNumber == customer_id
    ).first()
    if not customer:
        logger.warning(f"Customer not found: ID {customer_id}")
    return customer

# --- CREATE CUSTOMER ---
def create_customer(db: Session, customer: schemas.CustomerCreate):
    logger.info(f"Creating customer: {customer.customerName}")
    db_customer = models.Customer(**customer.model_dump())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

# --- UPDATE CUSTOMER ---
def update_customer(db: Session, customer_id: int, updates: schemas.CustomerUpdate):
    logger.info(f"Updating customer ID {customer_id}")
    db_customer = get_customer(db, customer_id)
    if not db_customer:
        return None
    for key, value in updates.model_dump(exclude_unset=True).items():
        setattr(db_customer, key, value)
    db.commit()
    db.refresh(db_customer)
    return db_customer

# --- DELETE CUSTOMER ---
def delete_customer(db: Session, customer_id: int):
    logger.info(f"Deleting customer ID {customer_id}")
    db_customer = get_customer(db, customer_id)
    if not db_customer:
        return None
    db.delete(db_customer)
    db.commit()
    return db_customer

# --- GET CUSTOMER ORDERS ---
def get_customer_orders(db: Session, customer_id: int):
    logger.info(f"Fetching orders for customer ID {customer_id}")
    return db.query(models.Order).filter(
        models.Order.customerNumber == customer_id
    ).all()

# --- GET CUSTOMER PAYMENTS ---
def get_customer_payments(db: Session, customer_id: int):
    logger.info(f"Fetching payments for customer ID {customer_id}")
    return db.query(models.Payment).filter(
        models.Payment.customerNumber == customer_id
    ).all()

# --- COUNT FUNCTIONS (Task 3) ---
def get_customers_count(db: Session):
    count = db.query(models.Customer).count()
    logger.info(f"Customers count query completed: {count}")
    return count

def get_orders_count(db: Session):
    count = db.query(models.Order).count()
    logger.info(f"Orders count query completed: {count}")
    return count

def get_payments_count(db: Session):
    count = db.query(models.Payment).count()
    logger.info(f"Payments count query completed: {count}")
    return count

def get_products_count(db: Session):
    count = db.scalar(text("SELECT COUNT(*) FROM products"))
    logger.info(f"Products count query completed: {count}")
    return count

def get_employees_count(db: Session):
    count = db.scalar(text("SELECT COUNT(*) FROM employees"))
    logger.info(f"Employees count query completed: {count}")
    return count

def get_offices_count(db: Session):
    count = db.scalar(text("SELECT COUNT(*) FROM offices"))
    logger.info(f"Offices count query completed: {count}")
    return count

def get_orderdetails_count(db: Session):
    count = db.scalar(text("SELECT COUNT(*) FROM orderdetails"))
    logger.info(f"Orderdetails count query completed: {count}")
    return count

def get_productlines_count(db: Session):
    count = db.scalar(text("SELECT COUNT(*) FROM productlines"))
    logger.info(f"Productlines count query completed: {count}")
    return count