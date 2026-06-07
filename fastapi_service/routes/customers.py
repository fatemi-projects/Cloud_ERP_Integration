# from fastapi import APIRouter, HTTPException
# from services.odoo_client import execute
# from core.logger import setup_logger

# logger = setup_logger()

# router = APIRouter()

# @router.get("/customers")
# def get_customers():
#     try:
#         data = execute(
#             "res.partner",
#             "search_read",
#             [[]],
#             {"fields": ["id", "name", "email", "phone"], "limit": 20}
#         )
#         logger.info("Fetching customers from Odoo")

#         return data

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


from fastapi import APIRouter, HTTPException
from services.odoo_client import execute
from core.logger import setup_logger
from core.security import verify_token
from fastapi import Depends
from pydantic import BaseModel

class CustomerCreate(BaseModel):
    name: str
    email: str = ""
    phone: str = ""

class CustomerUpdate(BaseModel):
    name: str = None
    email: str = None
    phone: str = None

logger = setup_logger()
router = APIRouter()

# ---------------- CLEAN HELPER ----------------
def clean_customer(record):
    return {
        "id": record.get("id"),
        "name": record.get("name") or "",
        "email": record.get("email") or "",
        "phone": record.get("phone") or "",
    }


# ---------------- GET CUSTOMERS ----------------
@router.get("/customers")
def get_customers(user=Depends(verify_token)):
    try:
        customers = execute(
            model="res.partner",
            method="search_read",
            args=[[]],
            kwargs={
                "fields": ["id", "name", "email", "phone"],
                "limit": 20
            },
        )

        logger.info("Fetching customers from Odoo")
        return [clean_customer(c) for c in customers]

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/customers")
def create_customer(customer: CustomerCreate):

    customer_id = execute(
        "res.partner",
        "create",
        [{
            "name": customer.name,
            "email": customer.email,
            "phone": customer.phone
        }]
    )

    logger.info("Create customer in Odoo with id", customer_id)
    return {
        "message": "Customer created successfully",
        "customer_id": customer_id
    }

@router.put("/customers/{customer_id}")
def update_customer(customer_id: int, customer: CustomerUpdate):

    update_data = {}

    if customer.name is not None:
        update_data["name"] = customer.name
    if customer.email is not None:
        update_data["email"] = customer.email
    if customer.phone is not None:
        update_data["phone"] = customer.phone

    execute(
        "res.partner",
        "write",
        [[customer_id], update_data]
    )

    logger.info("Update customer in Odoo with id", customer_id)
    return {
        "message": "Customer updated successfully",
        "customer_id": customer_id
    }

@router.delete("/customers/{customer_id}")
def delete_customer(customer_id: int):

    execute(
        "res.partner",
        "unlink",
        [[customer_id]]
    )

    logger.info("Deleted customer in Odoo with id", customer_id)
    return {
        "message": "Customer deleted successfully",
        "customer_id": customer_id
    }
