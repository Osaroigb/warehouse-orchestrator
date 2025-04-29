from fastapi import APIRouter
from app.routers import health
# from app.routers import orders, health


api_router = APIRouter()
api_router.include_router(health.router)
# api_router.include_router(orders.router, prefix="/orders", tags=["Orders"])