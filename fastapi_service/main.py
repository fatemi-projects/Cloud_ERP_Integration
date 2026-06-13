import os
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from routes.customers import router as customers_router
from routes.products import router as products_router
from routes.orders import router as orders_router
from core.logger import setup_logger
from core.security import create_token

# ---------------- APP ----------------
app = FastAPI(title="Cloud ERP Integration API")

logger = setup_logger()
logger.info("FastAPI app started")

# ---------------- BASE DIR ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ---------------- STATIC + TEMPLATES ----------------
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

app.mount(
    "/static",
    StaticFiles(directory=os.path.join(BASE_DIR, "static")),
    name="static"
)

# ---------------- HOME PAGE ----------------
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        name="index.html",
        context={},
        request=request
    )

# ---------------- LOGIN ----------------
@app.post("/login")
def login():
    token = create_token({"user": "admin"})
    logger.info("Creating Token")
    return {"access_token": token}

# ---------------- HEALTH CHECK ----------------
@app.get("/health")
def health_check():
    return {"status": "OK"}

# ---------------- API ROUTES ----------------
API_PREFIX = "/api/v1"

app.include_router(customers_router, prefix=API_PREFIX)
app.include_router(products_router, prefix=API_PREFIX)
app.include_router(orders_router, prefix=API_PREFIX)
