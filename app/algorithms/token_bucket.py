import time

from app.api.schemas import CheckResponse


class TokenBucket:

    def __init__(self, capacity: int, refill_rate: float):
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.current_tokens = capacity
        self.last_refill_time = time.time()

    def _refill(self):
        current_time = time.time()

        elapsed_time = current_time - self.last_refill_time

        new_tokens = elapsed_time * self.refill_rate

        self.current_tokens = min(
            self.capacity,
            self.current_tokens + new_tokens
        )

        self.last_refill_time = current_time

    def allow_request(self):
        self._refill()

        if self.current_tokens >= 1:
            self.current_tokens -= 1

            return CheckResponse(
                allowed=True,
                remaining=int(self.current_tokens),
                retry_after=0
            )

        return CheckResponse(
            allowed=False,
            remaining=0,
            retry_after=1 / self.refill_rate
        )