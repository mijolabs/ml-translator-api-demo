from fastapi import APIRouter, HTTPException

from app.polyglot import Polyglot
from app.schemas import (
    DetectionRequest,
    DetectionResult,
    TranslationRequest,
    TranslationResult
)



router = APIRouter()
polyglot = Polyglot()


@router.post("/detect")
async def detect(detection_request: DetectionRequest) -> DetectionResult:
    return polyglot.detect_language(detection_request)


@router.post("/translate")
async def translate(translation_request: TranslationRequest) -> TranslationResult:
    """
    Request body parameters `source` and `target` are optional.
    
    The endpoint will attempt to auto-detect the source language unless `source` is provided. The default `target` language is `en`.

    Currently supports `ru-en` and `zh-en`. 
    """
    if not translation_request.source:
        result = polyglot.detect_language(
            DetectionRequest(text=translation_request.text)
        )

        translation_request.source = result.language

    language_pair = f"{translation_request.source}-{translation_request.target}"

    if not language_pair in polyglot.valid_language_pairs:
        raise HTTPException(
            status_code=400, detail=f"Invalid language pair: {language_pair}"
        )

    return polyglot.generate_translation(translation_request)
