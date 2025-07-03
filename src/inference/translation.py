import logging
from collections.abc import Iterator
from typing import Any

import torch
from nltk import sent_tokenize
from transformers import MarianMTModel, MarianTokenizer
from transformers.generation.utils import GenerateOutput
from transformers.tokenization_utils_base import BatchEncoding

from core.constants import APP_ROOT
from core.exceptions import UnsupportedLanguagePairError
from dependencies.context import Context
from inference.models import TranslationResult


OPUS_MT_MODELS: dict[str, str] = {
    "ru-en": "inference/pretrained_models/opus-mt-ru-en",
    "zh-en": "inference/pretrained_models/opus-mt-zh-en",
}

DEFAULT_MAX_TOKENS_PER_BATCH = 256
MAX_NEW_TOKENS = 512
NUM_BEAMS = 2


def preload_opus_mt_models() -> dict:
    logging.info(f"Initializing OPUS-MT models: {[model for model in OPUS_MT_MODELS.keys()]}")

    models: dict[str, Any] = {}
    for language_pair, model_directory in OPUS_MT_MODELS.items():
        params: dict = {
            "pretrained_model_name_or_path": APP_ROOT / model_directory,
            "local_files_only": True,
        }

        tokenizer: MarianTokenizer = MarianTokenizer.from_pretrained(**params)
        model: MarianMTModel = MarianMTModel.from_pretrained(**params)
        model.eval()

        models[language_pair] = {"tokenizer": tokenizer, "model": model}

    return models


def translate_text(
    context: Context,
    source: str,
    target: str,
    text: str,
) -> TranslationResult:
    source, target = source.lower(), target.lower()
    if f"{source}-{target}" not in OPUS_MT_MODELS:
        raise UnsupportedLanguagePairError(
            f"Translation from '{source}' to '{target}' is not supported. "
            f"Supported pairs: {', '.join(OPUS_MT_MODELS.keys())}.",
        )

    return generate_translation(context=context, source=source, target=target, text=text)


@torch.inference_mode()
def generate_translation(
    context: Context,
    source: str,
    target: str,
    text: str,
) -> TranslationResult:
    language_pair: str = f"{source}-{target}"
    tokenizer: MarianTokenizer = context.inference.opus_mt[language_pair]["tokenizer"]
    model: MarianMTModel = context.inference.opus_mt[language_pair]["model"]

    sentences: list[str] = sent_tokenize(text)
    batches: Iterator[list[str]] = batch_by_token_count(tokenizer=tokenizer, sentences=sentences)

    translated_sentences: list[str] = []
    for batch in batches:
        encoded: BatchEncoding = tokenizer(
            text=batch,
            return_tensors="pt",
            padding=True,
            truncation=True,
        )
        output: GenerateOutput | torch.LongTensor = model.generate(
            input_ids=encoded["input_ids"],
            max_new_tokens=MAX_NEW_TOKENS,
            num_beams=NUM_BEAMS,
            early_stopping=True,
        )
        translated_sentences.extend(tokenizer.batch_decode(output, skip_special_tokens=True))

    return TranslationResult(source=source, target=target, result=" ".join(translated_sentences))


def batch_by_token_count(
    tokenizer: MarianTokenizer,
    sentences: list[str],
    max_tokens_per_batch: int = DEFAULT_MAX_TOKENS_PER_BATCH,
) -> Iterator[list[str]]:
    batch: list[str] = []
    token_count: int = 0

    for sentence in sentences:
        sentence_tokens: list[int] = tokenizer.encode(sentence, add_special_tokens=False)
        # If adding this sentence would exceed max_tokens_per_batch, yield current batch first
        if token_count + len(sentence_tokens) > max_tokens_per_batch and batch:
            yield batch
            batch, token_count = [], 0
        batch.append(sentence)
        token_count += len(sentence_tokens)

    if batch:
        yield batch
