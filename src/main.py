from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config import CONFIG
from src.data_models import TranslationRequest
from src.polyglot import Polyglot

config = CONFIG.api
polyglot = Polyglot()

app = FastAPI(
    title=config.title,
    version=config.version,
    description=config.description,
    docs_url=config.docs_endpoints.openapi,
    redoc_url=config.docs_endpoints.redoc,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.cors.origins,
    allow_credentials=config.cors.credentials,
    allow_methods=config.cors.methods,
    allow_headers=config.cors.headers,
)


@app.on_event("startup")
def startup():
    ...


@app.post("/detect/")
def detect():
    ...

@app.post("/translate/")
def translate(request: TranslationRequest):
    return
