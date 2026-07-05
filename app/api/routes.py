from fastapi import APIRouter
from app.api.schemas import CheckRequest
from app.services.rate_limiter_service import RateLimiterService  
router = APIRouter()
rate_limiter_service = RateLimiterService()


@router.get("/")
def root():
    return {
        "message": "Rate Limiter Service is running!"
    }


@router.post("/check")
def check_limit(request: CheckRequest):

    result = rate_limiter_service.check_limit(request)

    return result