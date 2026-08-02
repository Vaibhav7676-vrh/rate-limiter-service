from pathlib import Path
import time

from app.storage.redis_client import redis_client


class BucketRepository:

    def __init__(self):
        lua_path = Path(__file__).parent / "lua" / "token_bucket.lua"

        with open(lua_path, "r") as file:
            self.lua_script = file.read()

        # Load the Lua script once and cache its SHA1 hash
        self.script_sha = redis_client.script_load(self.lua_script)

    def check_rate_limit(
        self,
        bucket_key: str,
        capacity: int,
        refill_rate: float,
    ):

        return redis_client.evalsha(
            self.script_sha,
            1,
            bucket_key,
            capacity,
            refill_rate,
            time.time()
        )