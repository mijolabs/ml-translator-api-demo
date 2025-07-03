from dataclasses import dataclass
from typing import Annotated, Any

from fastapi import Depends, Request
from fasttext.FastText import _FastText as FastTextModel


@dataclass(slots=True)
class InferenceDependencies:
    fasttext: FastTextModel
    opus_mt: dict[str, dict[str, Any]]


@dataclass(slots=True)
class ContextContainer:
    request: Request
    inference: InferenceDependencies


async def get_context(request: Request) -> ContextContainer:
    return ContextContainer(request=request, inference=request.state.inference)


Context = Annotated[ContextContainer, Depends(get_context)]
