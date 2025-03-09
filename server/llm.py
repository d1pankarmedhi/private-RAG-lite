from typing import List

from config import LLM_CONTEXT_SIZE, LLM_GPU_LAYERS, LLM_THREADS, MODEL_PATH
from llama_cpp import Llama
from log_utils import logger


def phi3_llm(input_prompt: str, relevant_chunks: List[str]):
    """
    Generates a response using the Phi-3 language model.

    Args:
        input_prompt (str): The user's question or prompt.
        relevant_chunks (List[str]): Relevant document chunks retrieved from vector store.

    Returns:
        str: The cleaned output response from the language model.
    """
    logger.debug("Initializing Llama model.")
    llm = Llama(
        model_path=MODEL_PATH,
        n_ctx=LLM_CONTEXT_SIZE,
        n_threads=LLM_THREADS,
        n_gpu_layers=LLM_GPU_LAYERS,
    )

    prompt = f"""CONTENT: {relevant_chunks}\n\nQUESTION: {input_prompt}\n\nFrom the given CONTENT, Please answer the QUESTION."""

    logger.debug("Generating response from Phi-3 model.")
    output = llm(
        f"<|user|>\n{prompt}<|end|>\n<|assistant|>",
        max_tokens=LLM_CONTEXT_SIZE,
        stop=["<|end|>"],
        echo=True,
    )

    cleaned_output = output["choices"][0]["text"].split("<|assistant|>", 1)[-1].strip()
    logger.debug("Response cleaned and returned.")
    return cleaned_output
