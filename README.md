<div align="center">
  <h1>Private RAG Lite</h1>
  <p>A lightweight conversational RAG pipeline for your private documents.</p>
</div>

---

## 🚀 Overview

Private RAG Lite provides a simple and efficient way to interact with your personal documents using a conversational interface. It leverages powerful open-source tools to deliver accurate and context-aware responses, all within your local environment.

## 🛠️ Key Components

* **Embedding Model (Sentence Transformer):**
    * Documents are chunked using [Langchain Text Splitter](https://pypi.org/project/langchain-text-splitters/) (default chunk size: 500, overlap: 20).
    * Embeddings are generated with [sentence-transformers/all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) for efficient semantic encoding.
* **Vector Storage (ChromaDB):**
    * [ChromaDB](https://www.trychroma.com/) is used for local vector storage and fast similarity searches.
    * Cosine similarity is employed to retrieve the top k most relevant document chunks.
* **Language Model (GGUF Phi-3-mini-4k-instruct):**
    * [bartowski/Phi-3-medium-4k-instruct-GGUF](https://huggingface.co/bartowski/Phi-3-medium-4k-instruct-GGUF) powers the conversational responses.
    * Optimized for local systems and CPU environments.
    * **Q4_K_M** quantization is used for efficient inference.
    * **Important:** Download the model from the Hugging Face repository and place it in the `models` directory.

## ⚙️ Getting Started

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/d1pankarmedhi/private-RAG-lite.git
    cd private-rag-lite
    ```
2.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Download the Model:**
    * Download the `bartowski/Phi-3-medium-4k-instruct-GGUF` model in Q4_K_M format from Hugging Face.
    * Place the downloaded model file inside the `models` directory.
4.  **Run the Application:**
    * Follow the instructions in your application's `README` or run file to start the application.

## 📄 Usage

1.  **Upload Documents:**
    * Upload your private documents (PDF, TXT, etc.) through the application's interface.
2.  **Ask Questions:**
    * Enter your questions in the conversational interface.
3.  **Receive Answers:**
    * The system will retrieve relevant information from your documents and generate a response.

## 🔗 Demo

A live demo is available on Hugging Face Spaces: [phi-3-RAG](https://huggingface.co/spaces/dmedhi/phi-3-RAG)
* **Note:** Due to resource limitations on the free Hugging Face Spaces tier, it's recommended to use small PDF documents for optimal performance.

## 📝 Notes

* This project is designed for local use and privacy.
* Performance may vary based on your system's hardware.
* Feel free to contribute to this project.

---
