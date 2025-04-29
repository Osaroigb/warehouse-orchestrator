from fastapi import FastAPI
from app.routers import api_router
from app.core.database import init_db
from app.utils.errors import BaseError
from app.exception_handler import base_error_handler

app = FastAPI(title="Warehouse Orchestrator")

# Register exception handler
app.add_exception_handler(BaseError, base_error_handler)

# Register routes
app.include_router(api_router)

# Trigger on app startup
@app.on_event("startup")
async def on_startup():
    init_db()