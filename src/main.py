from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config import CONFIG
from src.routes import v1



config = CONFIG.api

app = FastAPI(
    title=config.title,
    version=config.version,
    description=config.description,
    docs_url=config.docs_endpoint.openapi,
    redoc_url=config.docs_endpoint.redoc,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.cors.origins,
    allow_credentials=config.cors.credentials,
    allow_methods=config.cors.methods,
    allow_headers=config.cors.headers,
)

app.include_router(v1.router, prefix="/v1", tags=["v1"])
