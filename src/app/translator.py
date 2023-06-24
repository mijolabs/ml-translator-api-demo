from collections import defaultdict

from box import Box
import fasttext
from nltk import sent_tokenize
import torch
from transformers import MarianMTModel, MarianTokenizer

from app.config import CONFIG
from app.schemas import (
    DetectionRequest,
    DetectionResult,
    TranslationRequest,
    TranslationResult
)


class Translator:    
    def __init__(self):
        self.__dict__.update(CONFIG.translator)

        self.fasttext = self.init_identification_model()
        self.models = self.init_translation_models()

        self.valid_language_pairs = {
            language_pair for language_pair in self.models.keys()
        }

    
    def init_identification_model(self) -> fasttext.FastText:
        model_filepath = f"{self.models.base_directory}/{self.models.identification}"
        fasttext.FastText.eprint = lambda x: None

        return fasttext.load_model(model_filepath)

    
    def init_translation_models(self) -> Box:
        print(
            f"[*] Initializing pretrained language models: {[model for model in self.models.translation.values()]}"
        )

        models = defaultdict(Box)
        
        for language_pair, model_name in self.models.translation.items():
            _params = {
                "pretrained_model_name_or_path": f"{self.models.base_directory}/{model_name}",
                "local_files_only": True
            }

            models[language_pair].tokenizer = MarianTokenizer.from_pretrained(**_params)
            models[language_pair].model = MarianMTModel.from_pretrained(**_params)

        return models


    def detect_language(self, detection_request: DetectionRequest) -> DetectionResult:
        language, probability = self.fasttext.predict(
            detection_request.text.lower().replace("\r\n", " ").replace("\n", " ").strip()
        )

        return DetectionResult(
            language=language[0].strip("__label__"),
            probability=min(1.0, probability[0])
        )


    @torch.no_grad()
    def generate_translation(self, translation_request: TranslationRequest) -> TranslationResult:
        language_pair = f"{translation_request.source}-{translation_request.target}"

        tokenizer = self.models[language_pair].tokenizer
        model = self.models[language_pair].model

        sentences = sent_tokenize(translation_request.text)

        batches = [
            sentences[start:start + self.max_batch_size]
            for start in range(0, len(sentences), self.max_batch_size)
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
