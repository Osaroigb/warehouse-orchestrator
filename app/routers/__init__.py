from fastapi import APIRouter
from app.routers.home_route import router as home_router
from app.routers.order_route import router as order_router

api_router = APIRouter()
api_router.include_router(home_router)
api_router.include_router(order_router)