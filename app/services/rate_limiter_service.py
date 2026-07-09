from app.algorithms.token_bucket import TokenBucket
from app.api.schemas import CheckRequest


class RateLimiterService:

    def __init__(self):

        self.buckets = {}

    def check_limit(self, request: CheckRequest):

        if request.api_key not in self.buckets:

            self.buckets[request.api_key] = TokenBucket(
                capacity=5,
                refill_rate=1
            )

        bucket = self.buckets[request.api_key]
        
        print(self.buckets)

        return bucket.allow_request()
    