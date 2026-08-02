from app.storage.redis_client import redis_client


class BucketRepository:
    """
    Repository responsible for storing and retrieving
    Token Bucket state from Redis.
    """

    def get_bucket(self, bucket_key: str) -> dict:
        """
        Retrieve bucket data from Redis.

        Returns:
            Dictionary containing bucket data.
            Returns {} if the bucket doesn't exist.
        """
        return redis_client.hgetall(bucket_key)

    def save_bucket(self, bucket_key: str, bucket_data: dict) -> None:
        """
        Save bucket state to Redis.

        Example bucket_data:
        {
            "current_tokens": 4,
            "last_refill_time": 1753862000.25
        }
        """
        redis_client.hset(
            bucket_key,
            mapping=bucket_data
        )

    def delete_bucket(self, bucket_key: str) -> None:
        """
        Delete a bucket from Redis.
        """
        redis_client.delete(bucket_key)

    def bucket_exists(self, bucket_key: str) -> bool:
        """
        Check whether a bucket exists.
        """
        return redis_client.exists(bucket_key) == 1