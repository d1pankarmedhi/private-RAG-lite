<div style="text-align: center">
<h1>Private RAG Lite</h1>
<p>A light weight conversational RAG pipeline for your private documents</p>
</div>

---

## Embedding Model (Sentence Transformer)

Uploaded documents get chunked using [Langchain Text Splitter](https://pypi.org/project/langchain-text-splitters/) with a default chunk size of 500 and overlap of 20. For generating the embeddings, a  [sentence-transformers/all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) is utilized for encoding the chunks. 

## Vector Storage (ChromaDB)
ChromaDB works well for local setup and inference. It uses cosine similarity to find the top k most relevant chunks from the knowledge base. 

## Language Model (GGUF Phi-3-mini-4k-instruct)
[bartowski/Phi-3-medium-4k-instruct-GGUF](https://huggingface.co/bartowski/Phi-3-medium-4k-instruct-GGUF) is well supported for most local systems and can run on CPU environments. **Q4_K_M** is utilized for generating responses from the retrieved content. 

**Note**: You must download the model from the hugginface repository and put that inside the `models` directory.

### Demo
A live demo is available at [here](https://huggingface.co/spaces/dmedhi/phi-3-RAG) but it is recommended to use tiny pdf documents since the machine uses a free tier of Huggingface spaces.
