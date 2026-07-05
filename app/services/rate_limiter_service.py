from app.api.schemas import CheckRequest

class RateLimiterService:

    def check_limit(self, request: CheckRequest):

        print("Tenant:", request.tenant_id)
        print("API Key:", request.api_key)
        print("Resource:", request.resource)

        return {
            "allowed": True,
            "remaining": 49,
            "retry_after": 0
        }