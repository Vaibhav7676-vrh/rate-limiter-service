from prometheus_client import Counter, Histogram

allowed_requests = Counter(
    "allowed_requests_total",
    "Total allowed requests"
)

blocked_requests = Counter(
    "blocked_requests_total",
    "Total blocked requests"
)

request_latency = Histogram(
    "request_latency_seconds",
    "API request latency"
)