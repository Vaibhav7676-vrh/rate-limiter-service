from app.algorithms.token_bucket import TokenBucket
from app.api.schemas import CheckRequest
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

        bucket_data = self.bucket_repository.get_bucket(bucket_key)

        if bucket_data:

            bucket = TokenBucket(
                capacity=5,
                refill_rate=1,
                current_tokens=float(bucket_data["current_tokens"]),
                last_refill_time=float(bucket_data["last_refill_time"])
            )

        else:

            bucket = TokenBucket(
                capacity=5,
                refill_rate=1
            )

        result = bucket.allow_request()

        self.bucket_repository.save_bucket(
            bucket_key,
            {
                "current_tokens": bucket.current_tokens,
                "last_refill_time": bucket.last_refill_time
            }
        )

        return result