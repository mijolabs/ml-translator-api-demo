from dataclasses import dataclass
from typing import Any

from fasttext.FastText import _FastText as FastText


@dataclass(slots=True)
class InferenceDependencies:
    lid: FastText
    nmt: dict[str, dict[str, Any]]
