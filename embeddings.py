from typing import List

import torch
from sentence_transformers import SentenceTransformer


class Embedding:
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

    @classmethod
    def encode_text(cls, text: str):
        return cls.model.encode(text)
