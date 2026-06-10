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
