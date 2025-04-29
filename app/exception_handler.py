from fastapi import Request
from app.core.config import logging
from app.utils.errors import BaseError
from fastapi.responses import JSONResponse
from app.utils.api_responses import build_error_response
from starlette.exceptions import HTTPException as StarletteHTTPException


async def base_error_handler(request: Request, exc: BaseError):
    return build_error_response(
        message=exc.message,
        status=exc.httpCode,
        data={
            "verbose_message": exc.verboseMessage,
            "error_type": exc.errorType,
        }
    )


async def not_found_handler(request: Request, exc: StarletteHTTPException):
    if request.url.path.startswith("/flasgger_static"):
        return JSONResponse(status_code=204, content="")

    logging.error("Route not found: %s", request.url.path)
    return build_error_response(message="Route not found", status=404)
