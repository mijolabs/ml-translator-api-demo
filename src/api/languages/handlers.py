from fastapi import APIRouter, Body

from dependencies.context import Context
from inference.detection import detect_language
from inference.models import DetectionResult, TranslationResult
from inference.translation import translate_text


router = APIRouter(prefix="/languages", tags=["Language Processing"])


@router.post("/detection", tags=["Detection"])
async def handle_detection(
    context: Context,
    text: str = Body(
        embed=True,
        max_length=512,
        examples=["Привет, это хороший день."],
    ),
) -> DetectionResult:
    return detect_language(context=context, text=text)


@router.post("/translation", tags=["Translation"])
async def handle_translation(
    context: Context,
    source: str | None = Body(
        embed=True,
        default=None,
        max_length=2,
        examples=["ru"],
    ),
    target: str = Body(
        embed=True,
        default="en",
        max_length=2,
        examples=["en"],
    ),
    text: str = Body(
        embed=True,
        max_length=512,
        examples=["Привет, это хороший день."],
    ),
) -> TranslationResult:
    """
    Request body parameters `source` and `target` are optional.

    If `source` is not provided, there will be an attempt to auto-detect the source language.
    The default `target` language is `en`. The API currently supports `ru-en` and `zh-en`.
    """
    if source is None:
        result: DetectionResult = detect_language(context=context, text=text)

    return translate_text(
        context=context,
        source=source or result.language,
        target=target,
        text=text,
    )
