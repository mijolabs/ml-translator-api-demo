from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI

from dependencies.context import InferenceDependencies
from inference.detection import preload_fasttext_model
from inference.translation import preload_opus_mt_models


@asynccontextmanager
async def enter_lifespan(_app: FastAPI) -> AsyncGenerator[dict[str, Any]]:
    yield {
        "inference": InferenceDependencies(
            fasttext=preload_fasttext_model(),
            opus_mt=preload_opus_mt_models(),
        ),
    }
