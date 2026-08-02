-- Redis Key
local bucket_key = KEYS[1]

-- Parameters
local capacity = tonumber(ARGV[1])
local refill_rate = tonumber(ARGV[2])
local current_time = tonumber(ARGV[3])

-- Read bucket data from Redis
local bucket = redis.call("HGETALL", bucket_key)

local current_tokens
local last_refill_time

if #bucket == 0 then
    current_tokens = capacity
    last_refill_time = current_time
else
    current_tokens = tonumber(bucket[2])
    last_refill_time = tonumber(bucket[4])
end

-- Calculate elapsed time
local elapsed_time = current_time - last_refill_time

-- Calculate new tokens
local new_tokens = elapsed_time * refill_rate

-- Refill bucket
current_tokens = math.min(
    capacity,
    current_tokens + new_tokens
)

-- Update refill time
last_refill_time = current_time

-- Check if request is allowed
if current_tokens >= 1 then

    current_tokens = current_tokens - 1

    redis.call(
        "HSET",
        bucket_key,
        "current_tokens",
        current_tokens,
        "last_refill_time",
        last_refill_time
    )

    redis.call("EXPIRE", bucket_key, 3600)

    return {
        1,
        current_tokens,
        0
    }

else

    redis.call(
        "HSET",
        bucket_key,
        "current_tokens",
        current_tokens,
        "last_refill_time",
        last_refill_time
    )
    redis.call("EXPIRE", bucket_key, 3600)

    return {
        0,
        current_tokens,
        (1 - current_tokens) / refill_rate
    }

end