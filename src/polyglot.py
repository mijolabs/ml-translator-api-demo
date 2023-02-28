from collections import defaultdict
from timeit import default_timer as timestamp
from typing import Union

from box import Box
import fasttext
from nltk import sent_tokenize
from transformers import MarianMTModel, MarianTokenizer

from src.config import CONFIG
from src.schemas import (
    DetectionRequest,
    DetectionResult,
    ErrorResponse,
    TranslationRequest,
    TranslationResult
)


class Polyglot:    
    def __init__(self):
        self.__dict__.update(CONFIG.polyglot)

        self.fasttext = self.init_detection_model()
        self.models = self.init_translation_models()

        self.valid_language_pairs = {
            language_pair for language_pair in self.models.keys()
        }

    
    def init_detection_model(self) -> fasttext.FastText:
        model_filepath = f"{self.models.base_path}/{self.models.detection}"
        fasttext.FastText.eprint = lambda x: None

        return fasttext.load_model(model_filepath)

    
    def init_translation_models(self) -> Box:
        print("[*] Initializing pretrained language models")
        models = defaultdict(Box)
        
        for language_pair, model_name in self.models.translation.items():
            _params = {
                "pretrained_model_name_or_path": f"{self.models.base_path}/{model_name}",
                "local_files_only": True
            }

            models[language_pair].tokenizer = MarianTokenizer.from_pretrained(**_params)
            models[language_pair].model = MarianMTModel.from_pretrained(**_params)
        
        return models

    
    def translate(
        self,
        translation_request: TranslationRequest
    ) -> Union[TranslationResult, ErrorResponse]:
        if not translation_request.source:
            result = self.detect_language(
                DetectionRequest(text=translation_request.text)
            )

            translation_request.source = result.language

        language_pair = f"{translation_request.source}-{translation_request.target}"

        if language_pair in self.valid_language_pairs:
            return self.generate_translation(translation_request)

        else:
            return ErrorResponse(error=f"invalid language pair: {language_pair}")


    def detect_language(self, detection_request: DetectionRequest) -> DetectionResult:
        language, probability = self.fasttext.predict(
            detection_request.text.lower().replace("\r\n", " ").replace("\n", " ").strip()
        )

        return DetectionResult(
            language=language[0].strip("__label__"),
            probability=min(1.0, probability[0])
        )


    def generate_translation(self, translation_request: TranslationRequest) -> TranslationResult:
        language_pair = f"{translation_request.source}-{translation_request.target}"

        tokenizer = self.models[language_pair].tokenizer
        model = self.models[language_pair].model

        sentences = sent_tokenize(translation_request.text)

        batches = [
            sentences[i:i + self.max_batch_size]
            for i in range(0, len(sentences), self.max_batch_size)
        ]
        
        translated_sentences = []

        for batch in batches:
            encoded = tokenizer.batch_encode_plus(batch, return_tensors="pt", padding=True)
            generated_output = model.generate(
                encoded["input_ids"],
                max_new_tokens=self.max_new_tokens,
                num_beams=self.num_beams,
                early_stopping=self.early_stopping,
                )

            translated_sentences.extend(
                tokenizer.batch_decode(generated_output, skip_special_tokens=True)
            )

        return TranslationResult(
            source=translation_request.source,
            target=translation_request.target,
            translation=" ".join(translated_sentences)
        )


if __name__ == "__main__":
    p = Polyglot()

    input_text = "Привет, это хороший день."

    _alpha = timestamp()
    result = p.translate(
        TranslationRequest(text=input_text)
    )
    print(result)
    print(f"[*] Time elapsed: {timestamp() - _alpha:.3}")
