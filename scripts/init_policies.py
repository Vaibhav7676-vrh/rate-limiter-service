from app.storage.policy_repository import PolicyRepository

repository = PolicyRepository()

repository.save_policy(
    tenant_id="twitter",
    resource="tweet",
    capacity=5,
    refill_rate=1,
)

repository.save_policy(
    tenant_id="instagram",
    resource="like",
    capacity=10,
    refill_rate=2,
)

repository.save_policy(
    tenant_id="facebook",
    resource="comment",
    capacity=20,
    refill_rate=5,
)

print("Policies initialized successfully!")