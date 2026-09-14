markdown
# Multi-Tenant Rate Limiter Service

A distributed rate limiter built with FastAPI and Redis, supporting per-tenant, per-resource rate limiting policies — similar to how production APIs (Stripe, GitHub) throttle usage per customer.

## Why this exists

Most simple rate limiters break under concurrent load: if two requests check "do I have tokens left?" at the same time, both can pass even when only one token remains. This project solves that by pushing the token bucket logic into Redis as an **atomic Lua script**, so the check-and-decrement happens as a single indivisible operation — no race conditions, even with many app instances hitting the same bucket.

## How it works

- **Algorithm:** Token bucket. Each `(tenant_id, resource)` pair gets its own bucket with a configurable `capacity` and `refill_rate`.
- **Atomicity:** The refill + check + decrement logic runs entirely inside a Redis Lua script (`app/storage/lua/token_bucket.lua`), executed as one atomic operation via `EVAL`. This is what makes it safe under concurrency — Redis guarantees Lua scripts run without interleaving.
- **Multi-tenancy:** Policies (capacity + refill rate) are stored per tenant and resource in Redis, so different customers or endpoints can have different limits without code changes.

## Tech stack

Python, FastAPI, Redis (Lua scripting), Docker Compose, Prometheus, Grafana, Locust (load testing)

## Architecture

Client → FastAPI (/check) → RateLimiterService → Redis (atomic Lua script)
↓
Prometheus metrics (allowed/blocked/latency)
↓
Grafana dashboard


## API

**POST** `/check`

```json
{
  "tenant_id": "facebook",
  "api_key": "12345fgh",
  "resource": "comment"
}
```

Response:
```json
{
  "allowed": true,
  "remaining": 42,
  "retry_after": 0
}
```

## Running it

```bash
docker compose up
```

This starts:
- `app` — FastAPI service on `:8000`
- `redis` — token bucket + policy storage on `:6379`
- `prometheus` — metrics scraping on `:9090`
- `grafana` — dashboards on `:3001`

Set a rate limit policy manually for testing:

```bash
docker compose exec redis redis-cli HSET policy:facebook:comment capacity 100 refill_rate 50
```

## Load testing

Load tested with Locust (`locustfile.py`), simulating concurrent users hitting `/check` for the same tenant/resource.

**Results:**

| Scenario | Users | RPS | p50 latency | p95 latency | Result |
|---|---|---|---|---|---|
| High capacity (no throttling) | 1,000 | ~1,900 | ~200ms | ~290ms | 0 failures — service handles sustained load cleanly |
| Constrained policy (capacity: 100, refill: 50/s) | 300 | ~1,000 | ~2ms | ~6ms | **94% of requests (55,552 / 59,108) correctly rejected with 429** once the bucket was exhausted |

The sharp latency drop under throttling (200ms → 2ms) reflects requests failing fast at the Redis layer instead of flowing through full request handling — the limiter protects the service from overload rather than just rejecting late.

Run it yourself:
```bash
locust -f locustfile.py --host http://localhost:8000
```

## Monitoring

Prometheus metrics exposed at `/metrics`:
- `allowed_requests_total`
- `blocked_requests_total`
- `request_latency` (histogram)

A Grafana dashboard visualizes these in real time — see screenshot below.

![Grafana Dashboard](docs/grafana-dashboard.png)

## Project structure

app/
├── algorithms/token_bucket.py # In-memory reference implementation
├── api/routes.py # FastAPI endpoints
├── storage/
│ ├── lua/token_bucket.lua # Atomic Redis implementation
│ ├── bucket_repository.py
│ └── policy_repository.py # Per-tenant policy storage
├── monitoring/metrics.py # Prometheus instrumentation
└── main.py
locustfile.py # Load testing config
docker-compose.yml # Full stack (app + redis + prometheus + grafana)

A few things to actually do before pasting this in:

Add a docs/ folder to your repo with your Grafana screenshot saved as grafana-dashboard.png, or just delete that image line if you don't want to bother with it.
Fill in your actual GitHub username if you want a clone command — I left that out since I didn't want to guess it wrong.
Double check the numbers table matches what you screenshot — I used the exact figures from your test.