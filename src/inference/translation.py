import logging
from collections.abc import Iterator
from typing import Any

import torch
from nltk import sent_tokenize
from transformers import MarianMTModel, MarianTokenizer

from api.dependencies import Context
from api.languages.models import TranslationResult
from inference.detection import DetectionResult, detect_language
from settings import APP_ROOT


NMT_MODELS: dict[str, str] = {
    "ru-en": "inference/pretrained_models/opus-mt-ru-en",
    "zh-en": "inference/pretrained_models/opus-mt-zh-ru",
}

DEFAULT_MAX_TOKENS_PER_BATCH = 256
MAX_NEW_TOKENS = 512
NUM_BEAMS = 2


def preload_nmt_models() -> dict:
    logging.info(f"Initializing translation models: {[model for model in NMT_MODELS.keys()]}")

    models: dict[str, Any] = {}
    for language_pair, model_directory in NMT_MODELS.items():
        params: dict = {
            "pretrained_model_name_or_path": APP_ROOT / model_directory,
            "local_files_only": True,
        }

        tokenizer: MarianTokenizer = MarianTokenizer.from_pretrained(**params)
        model: MarianMTModel = MarianMTModel.from_pretrained(**params)
        model.eval()

        models[language_pair] = {"tokenizer": tokenizer, "model": model}

    return models


async def translate_text(
    context: Context,
    source: str | None,
    target: str,
    text: str,
) -> TranslationResult:
    if source is None:
        result: DetectionResult = await detect_language(context=context, text=text)
        source = result.language

    language_pair: str = f"{source}-{target}"
    if not source or language_pair not in NMT_MODELS:
        raise ValueError

    return await generate_translation(
        context=context,
        source=source,
        target=target,
        text=text,
    )


@torch.inference_mode()
async def generate_translation(
    context: Context,
    source: str,
    target: str,
    text: str,
) -> TranslationResult:
    language_pair: str = f"{source}-{target}"
    tokenizer = context.inference.nmt[language_pair]["tokenizer"]
    model = context.inference.nmt[language_pair]["model"]

    sentences: list[str] = sent_tokenize(text)
    batches: Iterator[list[str]] = batch_by_token_count(
        tokenizer=tokenizer,
        sentences=sentences,
        max_tokens_per_batch=DEFAULT_MAX_TOKENS_PER_BATCH,
    )
    # batches: list[list[str]] = [
    #     sentences[start : start + MAX_BATCH_SIZE]
    #     for start in range(0, len(sentences), MAX_BATCH_SIZE)
    # ]

    translated_sentences: list[str] = []
    for batch in batches:
        encoded = tokenizer.batch_encode_plus(
            batch,
            return_tensors="pt",
            padding=True,
            truncation=True,
        )
        output = model.generate(
            encoded["input_ids"],
            max_new_tokens=MAX_NEW_TOKENS,
            num_beams=NUM_BEAMS,
            early_stopping=True,
        )
        translated_sentences.extend(tokenizer.batch_decode(output, skip_special_tokens=True))

    return TranslationResult(source=source, target=target, result=" ".join(translated_sentences))


def batch_by_token_count(
    tokenizer: MarianTokenizer,
    sentences: list[str],
    max_tokens_per_batch: int = 1000,
) -> Iterator[list[str]]:
    batch, token_count = [], 0
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
