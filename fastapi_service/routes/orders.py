from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.odoo_client import execute
from core.logger import setup_logger
from core.security import verify_token
from fastapi import Depends

logger = setup_logger()
router = APIRouter()

# ---------------- MODELS ----------------
class OrderCreate(BaseModel):
    partner_id: int


class OrderUpdate(BaseModel):
    partner_id: int = None
    state: str = None


# ---------------- CLEAN HELPER ----------------
def clean_order(record):
    partner = record.get("partner_id")
    customer_name = partner[1] if isinstance(partner, (list, tuple)) and len(partner) > 1 else ""

    return {
        "id": record.get("id"),
        "name": record.get("name") or "",
        "customer": customer_name,
        "amount_total": record.get("amount_total") or 0,
        "state": record.get("state") or "",
    }


# ---------------- GET ORDERS ----------------
@router.get("/orders")
def get_orders(user=Depends(verify_token)):
    try:
        orders = execute(
            model="sale.order",
            method="search_read",
            args=[[]],
            kwargs={
                "fields": ["id", "name", "partner_id", "amount_total", "state"],
                "limit": 20
            },
        )
        logger.info("Fetching orders from Odoo")

        return [clean_order(o) for o in orders]

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/orders")
def create_order(order: OrderCreate):

    order_id = execute(
        "sale.order",
        "create",
        [{
            "partner_id": order.partner_id
        }]
    )

    return {
        "message": "Order created successfully",
        "order_id": order_id
    }

@router.put("/orders/{order_id}")
def update_order(order_id: int, order: OrderUpdate):

    update_data = {}

    if order.partner_id is not None:
        update_data["partner_id"] = order.partner_id

    if order.state is not None:
        update_data["state"] = order.state

    execute(
        "sale.order",
        "write",
        [[order_id], update_data]
    )

    return {
        "message": "Order updated successfully",
        "order_id": order_id
    }

@router.delete("/orders/{order_id}")
def delete_order(order_id: int):

    execute(
        "sale.order",
        "unlink",
        [[order_id]]
    )

    return {
        "message": "Order deleted successfully",
        "order_id": order_id
    }

# from fastapi import APIRouter, HTTPException
# import xmlrpc.client
# import os
# from dotenv import load_dotenv
# from pydantic import BaseModel
# from services.odoo_client import execute



# load_dotenv()

# router = APIRouter()

# # ---------------- ODOO CONFIG ----------------
# ODOO_URL = os.getenv("ODOO_URL")
# ODOO_DB = os.getenv("ODOO_DB")
# ODOO_USERNAME = os.getenv("ODOO_USERNAME")
# ODOO_PASSWORD = os.getenv("ODOO_PASSWORD")


# # ---------------- HELPER ----------------
# def get_odoo_connection():
#     common = xmlrpc.client.ServerProxy(f"{ODOO_URL}/xmlrpc/2/common")
#     uid = common.authenticate(ODOO_DB, ODOO_USERNAME, ODOO_PASSWORD, {})

#     if not uid:
#         raise HTTPException(status_code=401, detail="Odoo authentication failed")

#     models = xmlrpc.client.ServerProxy(f"{ODOO_URL}/xmlrpc/2/object")
#     return uid, models


# # ---------------- CLEAN VALUE ----------------
# def clean_value(value):
#     if value in [False, None, "false", "False", ""]:
#         return ""
#     return value


# def clean_order(record):
#     return {
#         "id": record.get("id"),
#         "name": clean_value(record.get("name")),
#         "customer": clean_value(record.get("partner_id")[1] if record.get("partner_id") else ""),
#         "amount_total": record.get("amount_total") or 0,
#         "state": clean_value(record.get("state")),
#     }


# # ---------------- MODELS ----------------
# class OrderCreate(BaseModel):
#     partner_id: int


# class OrderUpdate(BaseModel):
#     partner_id: int = None
#     state: str = None


# # ---------------- GET ORDERS ----------------
# @router.get("/orders")
# def get_orders():
#     try:
#         uid, models = get_odoo_connection()

#         orders = models.execute_kw(
#             ODOO_DB,
#             uid,
#             ODOO_PASSWORD,
#             "sale.order",
#             "search_read",
#             [[]],
#             {
#                 "fields": ["id", "name", "partner_id", "amount_total", "state"],
#                 "limit": 20
#             },
#         )

#         return [clean_order(o) for o in orders]

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# # ---------------- CREATE ORDER ----------------

# class OrderCreate(BaseModel):
#     partner_id: int

# @router.post("/orders")
# def create_order(payload: OrderCreate):

#     if not payload.partner_id:
#         return {"error": "partner_id required"}

#     order_id = execute(
#         "sale.order",
#         "create",
#         [{
#             "partner_id": payload.partner_id
#         }]
#     )

#     return {"message": "created", "id": order_id}

# # ---------------- UPDATE ORDER ----------------
# @router.put("/orders/{order_id}")
# def update_order(order_id: int, payload: OrderUpdate):
#     try:
#         uid, models = get_odoo_connection()

#         update_data = {}

#         if payload.partner_id is not None:
#             update_data["partner_id"] = payload.partner_id

#         if payload.state is not None:
#             update_data["state"] = payload.state

#         if not update_data:
#             raise HTTPException(status_code=400, detail="No data to update")

#         models.execute_kw(
#             ODOO_DB,
#             uid,
#             ODOO_PASSWORD,
#             "sale.order",
#             "write",
#             [[order_id], update_data]
#         )

#         return {"message": "Order updated", "id": order_id}

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# # ---------------- DELETE ORDER ----------------
# @router.delete("/orders/{order_id}")
# def delete_order(order_id: int):
#     try:
#         uid, models = get_odoo_connection()

#         models.execute_kw(
#             ODOO_DB,
#             uid,
#             ODOO_PASSWORD,
#             "sale.order",
#             "unlink",
#             [[order_id]]
#         )

#         return {"message": "Order deleted", "id": order_id}

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))