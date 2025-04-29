from fastapi import Request
from app.utils.errors import BaseError
from app.utils.api_responses import build_error_response


async def base_error_handler(request: Request, exc: BaseError):
    return build_error_response(
        message=exc.message,
        status=exc.httpCode,
        data={
            "verbose_message": exc.verboseMessage,
            "error_type": exc.errorType,
        }
    )