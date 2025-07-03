import logging

import fasttext

from core.constants import APP_ROOT
from core.exceptions import LanguageDetectionError
from dependencies.context import Context
from inference.models import DetectionResult


FASTTEXT_MODEL_FILEPATH = "inference/pretrained_models/lid.176/lid.176.ftz"
MIN_PROBABILITY: float = 0.4


def preload_fasttext_model() -> fasttext.FastText._FastText:
    logging.info("Initializing FastText model")

    fasttext.FastText.eprint = lambda x: None  # Suppress useless warning in fasttext==0.9.2
    return fasttext.load_model(str(APP_ROOT / FASTTEXT_MODEL_FILEPATH))


def detect_language(context: Context, text: str) -> DetectionResult:
    ft: fasttext.FastText._FastText = context.inference.fasttext

    cleaned_text: str = text.replace("\r\n", " ").replace("\n", " ").strip()
    labels, probabilities, *_ = ft.predict(
        text=cleaned_text,
        threshold=MIN_PROBABILITY,
    )
    if not labels or not probabilities:
        raise LanguageDetectionError

    return DetectionResult(
        language=labels[0].strip("__label__"),
        probability=min(1.0, probabilities[0]),
    )
