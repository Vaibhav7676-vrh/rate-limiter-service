from fastapi import APIRouter
from app.api.schemas import CheckRequest, CheckResponse
from app.services.rate_limiter_service import RateLimiterService  
from fastapi import APIRouter, HTTPException


router = APIRouter()
rate_limiter_service = RateLimiterService()


@router.get("/")
def root():
    return {
        "message": "Rate Limiter Service is running!"
    }


@router.post("/check", response_model=CheckResponse)
def check_limit(request: CheckRequest):

    result = rate_limiter_service.check_limit(request)

    if not result.allowed:
        raise HTTPException(
            status_code=429,
            detail={
                "allowed": False,
                "remaining": result.remaining,
                "retry_after": result.retry_after   
            }
        )

    return result