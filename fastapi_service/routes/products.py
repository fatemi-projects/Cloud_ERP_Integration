from fastapi import APIRouter, HTTPException
from services.odoo_client import execute
from core.logger import setup_logger
from core.security import verify_token
from fastapi import Depends
from pydantic import BaseModel

class ProductCreate(BaseModel):
    name: str
    price: float = 0

class ProductUpdate(BaseModel):
    name: str = None
    price: float = None


logger = setup_logger()
router = APIRouter()


# ---------------- CLEAN HELPER ----------------
def clean_product(record):
    return {
        "id": record.get("id"),
        "name": record.get("name") or "",
        "price": record.get("list_price") or 0
    }


# ---------------- GET PRODUCTS ----------------
@router.get("/products")
def get_products(user=Depends(verify_token)):
    try:
        products = execute(
            model="product.template",
            method="search_read",
            args=[[]],
            kwargs={
                "fields": ["id", "name", "list_price"],
                "limit": 20
            },
        )
        logger.info("Fetching products from Odoo")

        return [clean_product(p) for p in products]

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/products")
def create_product(product: ProductCreate):

    product_id = execute(
        "product.template",
        "create",
        [{
            "name": product.name,
            "list_price": product.price
        }]
    )

    return {
        "message": "Product created successfully",
        "product_id": product_id
    }

@router.put("/products/{product_id}")
def update_product(product_id: int, product: ProductUpdate):

    update_data = {}

    if product.name is not None:
        update_data["name"] = product.name
    if product.price is not None:
        update_data["list_price"] = product.price

    execute(
        "product.template",
        "write",
        [[product_id], update_data]
    )

    return {
        "message": "Product updated successfully",
        "product_id": product_id
    }

@router.delete("/products/{product_id}")
def delete_product(product_id: int):

    execute(
        "product.template",
        "unlink",
        [[product_id]]
    )

    return {
        "message": "Product deleted successfully",
        "product_id": product_id
    }
