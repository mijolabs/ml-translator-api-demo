from dataclasses import dataclass
from typing import Annotated

from fastapi import Depends, Request

from inference.dependencies import InferenceDependencies


@dataclass(slots=True)
class ContextContainer:
    request: Request
    inference: InferenceDependencies


async def get_context(request: Request) -> ContextContainer:
    return ContextContainer(request=request, inference=request.state.context)


Context = Annotated[ContextContainer, Depends(get_context)]
