from fastapi import FastAPI
from app.routers import api_router
from app.core.database import init_db
from app.utils.errors import BaseError
from contextlib import asynccontextmanager
from app.exception_handler import base_error_handler, not_found_handler
from starlette.exceptions import HTTPException as StarletteHTTPException

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(title="Warehouse Orchestrator", lifespan=lifespan)

# Exception Handlers
app.add_exception_handler(BaseError, base_error_handler)
app.add_exception_handler(StarletteHTTPException, not_found_handler)

# Routers
app.include_router(api_router)