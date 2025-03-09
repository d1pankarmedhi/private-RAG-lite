import os

MODEL_PATH = os.path.join(
    os.getcwd(),
    "models",
    "Phi-3.1-mini-4k-instruct-Q4_K_M.gguf",
)
LLM_CONTEXT_SIZE = 2000
LLM_THREADS = 1
LLM_GPU_LAYERS = 0
COLLECTION_NAME = "pdf_store"
CHUNK_SIZE_DEFAULT = 500
CHUNK_OVERLAP_DEFAULT = 20
