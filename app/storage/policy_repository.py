from app.storage.redis_client import redis_client


class PolicyRepository:

    def get_policy(
        self,
        tenant_id: str,
        resource: str,
    ):

        policy_key = f"policy:{tenant_id}:{resource}"

        policy = redis_client.hgetall(policy_key)

        if not policy:
            return None

        return {
            "capacity": int(policy["capacity"]),
            "refill_rate": float(policy["refill_rate"])
        }

    def save_policy(
        self,
        tenant_id: str,
        resource: str,
        capacity: int,
        refill_rate: float,
    ):

        policy_key = f"policy:{tenant_id}:{resource}"

        redis_client.hset(
            policy_key,
            mapping={
                "capacity": capacity,
                "refill_rate": refill_rate
            }
        )

    def delete_policy(
        self,
        tenant_id: str,
        resource: str,
    ):

        policy_key = f"policy:{tenant_id}:{resource}"

        redis_client.delete(policy_key)