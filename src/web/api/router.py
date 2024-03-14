from fastapi.routing import APIRouter

from src.web.api import contacts

api_router = APIRouter()
api_router.include_router(contacts.router, prefix="/contacts", tags=["contacts"])
