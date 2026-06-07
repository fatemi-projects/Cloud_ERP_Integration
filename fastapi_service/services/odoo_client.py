import xmlrpc.client
import os
from dotenv import load_dotenv
from fastapi import HTTPException

load_dotenv()

ODOO_URL = os.getenv("ODOO_URL")
ODOO_DB = os.getenv("ODOO_DB")
ODOO_USERNAME = os.getenv("ODOO_USERNAME")
ODOO_PASSWORD = os.getenv("ODOO_PASSWORD")


def get_models():
    common = xmlrpc.client.ServerProxy(f"{ODOO_URL}/xmlrpc/2/common")
    uid = common.authenticate(ODOO_DB, ODOO_USERNAME, ODOO_PASSWORD, {})

    if not uid:
        raise HTTPException(status_code=401, detail="Auth failed")

    models = xmlrpc.client.ServerProxy(f"{ODOO_URL}/xmlrpc/2/object")
    return uid, models


def execute(model, method, args=None, kwargs=None):
    uid, models = get_models()

    return models.execute_kw(
        ODOO_DB,
        uid,
        ODOO_PASSWORD,
        model,
        method,
        args or [],
        kwargs or {}
    )

# # import xmlrpc.client
# # from fastapi import HTTPException
# # from fastapi_service.core.config import (
# #     ODOO_URL,
# #     ODOO_DB,
# #     ODOO_USERNAME,
# #     ODOO_PASSWORD,
# # )

# # # ---------------- ODOO CONNECTION ----------------
# # def get_odoo_connection():
# #     try:
# #         common = xmlrpc.client.ServerProxy(f"{ODOO_URL}/xmlrpc/2/common")

# #         uid = common.authenticate(
# #             ODOO_DB,
# #             ODOO_USERNAME,
# #             ODOO_PASSWORD,
# #             {}
# #         )

# #         if not uid:
# #             raise HTTPException(
# #                 status_code=401,
# #                 detail="Odoo authentication failed"
# #             )

# #         models = xmlrpc.client.ServerProxy(f"{ODOO_URL}/xmlrpc/2/object")

# #         return uid, models

# #     except Exception as e:
# #         raise HTTPException(status_code=500, detail=str(e))


# import xmlrpc.client
# import os
# from dotenv import load_dotenv
# from fastapi import HTTPException

# load_dotenv()

# ODOO_URL = os.getenv("ODOO_URL")
# ODOO_DB = os.getenv("ODOO_DB")
# ODOO_USERNAME = os.getenv("ODOO_USERNAME")
# ODOO_PASSWORD = os.getenv("ODOO_PASSWORD")


# def get_odoo():
#     common = xmlrpc.client.ServerProxy(f"{ODOO_URL}/xmlrpc/2/common")
#     uid = common.authenticate(ODOO_DB, ODOO_USERNAME, ODOO_PASSWORD, {})

#     if not uid:
#         raise HTTPException(status_code=401, detail="Odoo auth failed")

#     models = xmlrpc.client.ServerProxy(f"{ODOO_URL}/xmlrpc/2/object")
#     return uid, models


# def execute(model, method, args, kwargs=None):
#     uid, models = get_odoo()

#     if kwargs is None:
#         kwargs = {}

#     try:
#         return models.execute_kw(
#             ODOO_DB,
#             uid,
#             ODOO_PASSWORD,
#             model,
#             method,
#             args,
#             kwargs
#         )
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))