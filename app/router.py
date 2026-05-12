from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import crud, schemas
from app.database import get_db
import logging
import asyncio
import time

logger = logging.getLogger(__name__)

router = APIRouter()

# --- GET ALL CUSTOMERS ---
@router.get("/", response_model=List[schemas.CustomerOut])
def list_customers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    logger.info(f"GET /customers - skip={skip} limit={limit}")
    customers = crud.get_customers(db, skip=skip, limit=limit)
    logger.info(f"Returned {len(customers)} customers")
    return customers


# --- CREATE CUSTOMER ---
@router.post("/", response_model=schemas.CustomerOut)
def create_customer(customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    logger.info(f"POST /customers - creating {customer.customerName}")
    return crud.create_customer(db, customer)


# --- COUNT ENDPOINTS (must be before /{customer_id}) ---
@router.get("/count")
def count_customers(db: Session = Depends(get_db)):
    logger.info("GET /customers/count")
    return {"customers": crud.get_customers_count(db)}

@router.get("/orders/count")
def count_orders(db: Session = Depends(get_db)):
    logger.info("GET /orders/count")
    return {"orders": crud.get_orders_count(db)}

@router.get("/products/count")
def count_products(db: Session = Depends(get_db)):
    logger.info("GET /products/count")
    return {"products": crud.get_products_count(db)}

@router.get("/employees/count")
def count_employees(db: Session = Depends(get_db)):
    logger.info("GET /employees/count")
    return {"employees": crud.get_employees_count(db)}

@router.get("/offices/count")
def count_offices(db: Session = Depends(get_db)):
    logger.info("GET /offices/count")
    return {"offices": crud.get_offices_count(db)}

@router.get("/payments/count")
def count_payments(db: Session = Depends(get_db)):
    logger.info("GET /payments/count")
    return {"payments": crud.get_payments_count(db)}

@router.get("/orderdetails/count")
def count_orderdetails(db: Session = Depends(get_db)):
    logger.info("GET /orderdetails/count")
    return {"orderdetails": crud.get_orderdetails_count(db)}

@router.get("/productlines/count")
def count_productlines(db: Session = Depends(get_db)):
    logger.info("GET /productlines/count")
    return {"productlines": crud.get_productlines_count(db)}


# --- OVERALL COUNTS WITH CONCURRENCY ---
@router.get("/overall_counts")
async def overall_counts(db: Session = Depends(get_db)):
    logger.info("GET /overall_counts - starting all 8 queries simultaneously")
    start_time = time.time()

    results = await asyncio.gather(
        asyncio.to_thread(crud.get_customers_count, db),
        asyncio.to_thread(crud.get_orders_count, db),
        asyncio.to_thread(crud.get_products_count, db),
        asyncio.to_thread(crud.get_employees_count, db),
        asyncio.to_thread(crud.get_offices_count, db),
        asyncio.to_thread(crud.get_payments_count, db),
        asyncio.to_thread(crud.get_orderdetails_count, db),
        asyncio.to_thread(crud.get_productlines_count, db),
    )

    end_time = time.time()
    logger.info(f"asyncio.gather() completed in {end_time - start_time:.3f} seconds")

    return {
        "customers": results[0],
        "orders": results[1],
        "products": results[2],
        "employees": results[3],
        "offices": results[4],
        "payments": results[5],
        "orderdetails": results[6],
        "productlines": results[7],
    }


# --- DYNAMIC ROUTES LAST ---
@router.get("/{customer_id}", response_model=schemas.CustomerOut)
def get_customer(customer_id: int, db: Session = Depends(get_db)):
    logger.info(f"GET /customers/{customer_id}")
    customer = crud.get_customer(db, customer_id)
    if not customer:
        logger.error(f"Customer ID {customer_id} not found")
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer


@router.put("/{customer_id}", response_model=schemas.CustomerOut)
def update_customer(customer_id: int, updates: schemas.CustomerUpdate, db: Session = Depends(get_db)):
    logger.info(f"PUT /customers/{customer_id}")
    customer = crud.update_customer(db, customer_id, updates)
    if not customer:
        logger.error(f"Customer ID {customer_id} not found for update")
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer


@router.delete("/{customer_id}", response_model=schemas.CustomerOut)
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    logger.info(f"DELETE /customers/{customer_id}")
    customer = crud.delete_customer(db, customer_id)
    if not customer:
        logger.error(f"Customer ID {customer_id} not found for delete")
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer


@router.get("/{customer_id}/orders", response_model=List[schemas.OrderOut])
def get_customer_orders(customer_id: int, db: Session = Depends(get_db)):
    logger.info(f"GET /customers/{customer_id}/orders")
    return crud.get_customer_orders(db, customer_id)


@router.get("/{customer_id}/payments", response_model=List[schemas.PaymentOut])
def get_customer_payments(customer_id: int, db: Session = Depends(get_db)):
    logger.info(f"GET /customers/{customer_id}/payments")
    return crud.get_customer_payments(db, customer_id)