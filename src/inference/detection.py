import fasttext

from api.dependencies import Context
from api.languages.models import DetectionResult
from settings import APP_ROOT


LID_MODEL_FILEPATH = "inference/pretrained_models/lid.176/lid.176.ftz"


def preload_lid_model() -> fasttext.FastText._FastText:
    fasttext.FastText.eprint = lambda x: None  # Suppress useless warning in fasttext==0.9.2
    return fasttext.load_model(str(APP_ROOT / LID_MODEL_FILEPATH))


async def detect_language(context: Context, text: str) -> DetectionResult:
    lid: fasttext.FastText._FastText = context.inference.lid
    language, probability = lid.predict(
        text.lower().replace("\r\n", " ").replace("\n", " ").strip()
    )

    if not language or not probability:
        raise ValueError("Language detection failed.")

    return DetectionResult(
        language=language[0].strip("__label__"),
        probability=min(1.0, probability[0]),
    )
