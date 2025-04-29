from fastapi import APIRouter, Depends
from fastapi.responses import Response
from app.utils.rate_limiting import rate_limiter
from app.utils.api_responses import build_success_response

router = APIRouter()

@router.get("/", tags=["Health"])
async def home(_: None = Depends(rate_limiter)):
    return build_success_response(message="Warehouse Orchestrator is running ✅")


@router.get("/health", tags=["Health"])
async def health_check(_: None = Depends(rate_limiter)):
    return build_success_response(message="Warehouse Orchestrator is running ✅")


@router.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return Response(status_code=204)

# @router.get("/", tags=["Health"])
# @router.get("/health", dependencies=[Depends(rate_limiter)], tags=["Health"])
# async def health_check():
#     return build_success_response(message="Warehouse Orchestrator is running ✅")