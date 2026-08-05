from fastapi import FastAPI
from app.api.routes import router
from prometheus_client import make_asgi_app
from starlette.middleware.wsgi import WSGIMiddleware

app =  FastAPI()

metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

app.include_router(router)

