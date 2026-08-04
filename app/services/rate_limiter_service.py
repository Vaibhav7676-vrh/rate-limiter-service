from app.api.schemas import CheckRequest, CheckResponse
from app.storage.bucket_repository import BucketRepository
from app.storage.policy_repository import PolicyRepository


class RateLimiterService:

    def __init__(self):
        self.bucket_repository = BucketRepository()
        self.policy_repository = PolicyRepository()

    def check_limit(self, request: CheckRequest):

        policy = self.policy_repository.get_policy(
            tenant_id=request.tenant_id,
            resource=request.resource,
        )

        if policy is None:
            return CheckResponse(
                allowed=False,
                remaining=0,
                retry_after=0
            )

        bucket_key = (
            f"{request.tenant_id}:"
            f"{request.api_key}:"
            f"{request.resource}"
        )

        result = self.bucket_repository.check_rate_limit(
            bucket_key=bucket_key,
            capacity=policy["capacity"],
            refill_rate=policy["refill_rate"],
        )

        return CheckResponse(
            allowed=bool(result[0]),
            remaining=int(float(result[1])),
            retry_after=round(float(result[2]), 2)
        )