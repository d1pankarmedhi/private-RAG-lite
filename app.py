import datetime
import os
import uuid

import fitz
import streamlit as st
from langchain_text_splitters import RecursiveCharacterTextSplitter
from llama_cpp import Llama

from datastore import ChromaStore
from embeddings import Embedding

#### state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "document_submitted" not in st.session_state:
    st.session_state.document_submitted = False


def phi3(input: str, relevant_chunks: list):
    llm = Llama(
        model_path=os.path.join(
            os.getcwd(),
            "models",
            "Phi-3.1-mini-4k-instruct-Q4_K_M.gguf",
        ),
        n_ctx=2000,
        n_threads=1,  # The number of CPU threads to use,
        n_gpu_layers=0,  # The number of layers to offload to GPU,
    )

    prompt = f"""CONTENT: {relevant_chunks}\n\nQUESTION: {input}\n\nFrom the given CONTENT, Please answer the QUESTION."""

    output = llm(
        f"<|user|>\n{prompt}<|end|>\n<|assistant|>",
        max_tokens=2000,
        stop=["<|end|>"],
        echo=True,
    )

    cleaned_output = output["choices"][0]["text"].split("<|assistant|>", 1)[-1].strip()
    return cleaned_output


def generate_unique_id():
    unique_id = uuid.uuid4()
    current_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
    combined_id = f"{unique_id}-{current_time}"
    return combined_id


def add_to_vectorstore(content: str, chunk_size: int = 500, chunk_overlap: int = 20):
    chromastore = ChromaStore(collection_name="pdf_store")

    # delete if already exist
    if "pdf_store" in chromastore.list_collections():
        chromastore.delete("pdf_store")
        st.toast("Old database cleaned!")
    collection = chromastore.create()
    # chunkify content
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        is_separator_regex=False,
    )
    chunks = text_splitter.split_text(content)

    # generate embeddings and ids
    embeddings, ids = [], []
    for i, chunk in enumerate(chunks):
        embeddings.append(Embedding.encode_text(chunk).tolist())
        ids.append(generate_unique_id())

    # add to vectorstore
    chromastore.add(
        collection=collection,
        embeddings=embeddings,
        documents=chunks,
        ids=ids,
    )


def similarity_search(query: str):
    chromastore = ChromaStore(collection_name="pdf_store")
    collection = chromastore.create()
    query_embedding = Embedding.encode_text(query).tolist()
    return chromastore.query(collection=collection, query_embedding=query_embedding)


def main():
    st.set_page_config(page_icon="🤖", page_title="Phi 3 RAG", layout="wide")
    st.markdown(
        """<h1 style="text-align:center;">Phi 3 RAG</h1>""", unsafe_allow_html=True
    )
    st.markdown(
        """<h3 style="text-align:center;">Conversational RAG application that utilizes local stack, <a href="https://huggingface.co/bartowski/Phi-3-medium-4k-instruct-GGUF">Phi-3 mini 4k instruct GGUF</a> and <a href="https://docs.trychroma.com/getting-started">ChromaDB</h3>""",
        unsafe_allow_html=True,
    )
    layout = st.columns(2)

    with layout[0]:
        with st.container(border=True, height=550):
            uploaded_file = st.file_uploader(
                label="Upload document to search",
                type="PDF",
                accept_multiple_files=False,
            )
            submit = st.button("submit")

            chunk_size = st.slider(
                label="Chunk_size", min_value=100, max_value=2000, step=100
            )
            chunk_overlap = st.slider(
                label="Chunk overlap", min_value=10, max_value=500, step=10
            )
            if uploaded_file is not None and submit is not False:
                # load in vectorstore
                doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
                text = ""
                for page in doc:
                    text += page.get_text()
                doc.close()

                # add to vectorstore
                add_to_vectorstore(text, chunk_size, chunk_overlap)
                st.session_state.document_submitted = True
                st.toast("Document added successfully added to vectorstore", icon="✅")

    # chats
    with layout[1]:
        with st.container(border=True, height=550):
            if st.session_state.document_submitted:
                user_input = st.chat_input("Ask me!")
                if user_input is not None:
                    st.session_state.chat_history.append(
                        {"role": "user", "content": str(user_input)}
                    )

                    with st.spinner("Thinking..."):
                        # find on vector store
                        relevant_chunks = similarity_search(user_input)
                        response = phi3(
                            input=user_input, relevant_chunks=relevant_chunks
                        )
                        st.session_state.chat_history.append(
                            {"role": "assistant", "content": str(response)}
                        )

                # display messages
                for message in reversed(st.session_state.chat_history):
                    with st.chat_message(message["role"]):
                        st.markdown(message["content"])


if __name__ == "__main__":
    main()
