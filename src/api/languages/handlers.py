from fastapi import APIRouter

from api.dependencies import Context
from api.languages.models import (
    DetectionRequest,
    DetectionResult,
    TranslationRequest,
    TranslationResult,
)
from inference.detection import detect_language
from inference.translation import translate_text


router = APIRouter(prefix="/languages", tags=["Language Processing"])


@router.post("/detection", tags=["Detection"])
async def handle_detection(context: Context, request: DetectionRequest) -> DetectionResult:
    return await detect_language(context=context, text=request.text)


@router.post("/translation", tags=["Translation"])
async def handle_translation(context: Context, request: TranslationRequest) -> TranslationResult:
    """
    Request body parameters `source` and `target` are optional.

    If `source` is not provided, there will be an attempt to auto-detect the source language.
    The default `target` language is `en`. The API currently supports `ru-en` and `zh-en`.
    """
    return await translate_text(
        context=context,
        source=request.source,
        target=request.target,
        text=request.text,
    )
