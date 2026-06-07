import os
from dotenv import load_dotenv

load_dotenv()

# ---------------- ODOO CONFIG ----------------
ODOO_URL = os.getenv("ODOO_URL")
ODOO_DB = os.getenv("ODOO_DB")
ODOO_USERNAME = os.getenv("ODOO_USERNAME")
ODOO_PASSWORD = os.getenv("ODOO_PASSWORD")

# ---------------- APP SETTINGS ----------------
APP_NAME = "Cloud ERP Integration"
DEBUG = True