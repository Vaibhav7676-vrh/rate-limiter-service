from fastapi import APIRouter, HTTPException
from app.api.schemas import CheckRequest, CheckResponse
from app.services.rate_limiter_service import RateLimiterService
import time

from app.monitoring.metrics import (
    allowed_requests,
    blocked_requests,
    request_latency,
)

router = APIRouter()
rate_limiter_service = RateLimiterService()


@router.get("/")
def root():
    return {
        "message": "Rate Limiter Service is running!"
    }


@router.post("/check")
def check_limit(request: CheckRequest):

    start_time = time.perf_counter()

    result = rate_limiter_service.check_limit(request)

    request_latency.observe(
        time.perf_counter() - start_time
    )

    if result.allowed:
        allowed_requests.inc()
        return result

    blocked_requests.inc()

    raise HTTPException(
        status_code=429,
        detail={
            "allowed": False,
            "remaining": result.remaining,
            "retry_after": result.retry_after
        }
    )