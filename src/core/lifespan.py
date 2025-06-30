from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI

from inference.dependencies import InferenceDependencies
from inference.detection import preload_lid_model
from inference.translation import preload_nmt_models


@asynccontextmanager
async def enter_lifespan(_app: FastAPI) -> AsyncGenerator[dict[str, Any]]:
    yield {
        "inference": InferenceDependencies(
            lid=preload_lid_model(),
            nmt=preload_nmt_models(),
        )
    }
