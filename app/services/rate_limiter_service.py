from app.api.schemas import CheckRequest, CheckResponse
from app.storage.bucket_repository import BucketRepository


class RateLimiterService:

    def __init__(self):
        self.bucket_repository = BucketRepository()

    def check_limit(self, request: CheckRequest):

        bucket_key = (
            f"{request.tenant_id}:"
            f"{request.api_key}:"
            f"{request.resource}"
        )

        result = self.bucket_repository.check_rate_limit(
            bucket_key=bucket_key,
            capacity=5,
            refill_rate=1
        )

        return CheckResponse(
            allowed=bool(result[0]),
            remaining=int(float(result[1])),
            retry_after=round(float(result[2]), 2)
        )