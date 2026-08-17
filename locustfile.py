from locust import HttpUser, task, between


class RateLimiterUser(HttpUser):
    wait_time = between(0.1, 0.5)

    @task
    def check_rate_limit(self):
        self.client.post(
            "/check",
            json={
                "tenant_id": "facebook",
                "api_key": "12345fgh",
                "resource": "comment"
            }
        )