import torch
from log_utils import logger
from sentence_transformers import SentenceTransformer


class Embedding:
    # Check device availability
    device = "cuda" if torch.cuda.is_available() else "cpu"
    logger.info(f"Using device for SentenceTransformer: {device}")

    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2", device=device)
    logger.info("SentenceTransformer model initialized with device.")

    @classmethod
    def encode_text(cls, text: str):
        logger.debug(
            "Encoding text using SentenceTransformer model with torch.autocast."
        )
        # Enable autocast for CUDA devices
        with torch.autocast(
            device_type=cls.device, dtype=torch.float16, enabled=cls.device == "cuda"
        ):
            embeddings = cls.model.encode(text)
        return embeddings
