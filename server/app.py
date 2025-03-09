import fitz
from embedding import Embedding
from fastapi import Depends, FastAPI, File, UploadFile
from langchain_text_splitters import RecursiveCharacterTextSplitter
from llm import phi3_llm
from log_utils import logger
from schema import ChatRequest, UploadConfig
from utils import *
from vectorstore import (
    add_to_vectorstore,
    create_vectorstore_collection,
    delete_vectorstore_collection,
    query_vectorstore,
)

app = FastAPI()
logger.info("FastAPI application initialized.")


@app.post("/upload_document/")
async def upload_document(
    upload_config: UploadConfig = Depends(),
    file: UploadFile = File(...),
):
    if file.content_type != "application/pdf":
        logger.warning("Invalid file type uploaded. Expected PDF.")
        return {"error": "Please upload a PDF file"}

    try:
        # generate unique ID
        doc_id = "doc_" + generate_unique_id()
        logger.info(f"Processing document upload with ID: {doc_id}")

        # read and extract text from PDF
        doc = fitz.open(stream=await file.read(), filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        logger.debug("Document text extracted.")

        # clean old database before adding new one
        delete_vectorstore_collection()
        collection = create_vectorstore_collection()

        # chunkify content
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=upload_config.chunk_size,
            chunk_overlap=upload_config.chunk_overlap,
            length_function=len,
            is_separator_regex=False,
        )
        chunks = text_splitter.split_text(text)
        logger.debug(f"Document chunked into {len(chunks)} chunks.")

        # generate embeddings and ids
        embeddings, ids = [], []
        for chunk in chunks:
            embeddings.append(Embedding.encode_text(chunk).tolist())
            ids.append(generate_unique_id())  # Chunk-specific IDs, still needed
        logger.debug("Embeddings generated for document chunks.")

        # add to vectorstore
        add_to_vectorstore(
            collection=collection,
            embeddings=embeddings,
            documents=chunks,
            ids=ids,
            doc_id=doc_id,
        )

        logger.info(f"Document with ID: {doc_id} successfully added to vectorstore.")
        return {
            "message": "Document successfully added to vectorstore",
            "document_id": doc_id,
        }  # Return document ID
    except Exception as e:
        logger.error(f"Error processing document: {e}")
        return {"error": f"Error processing document: {e}"}


def similarity_search_function(query: str):
    """
    Performs similarity search in the ChromaDB vector store.

    Args:
        query (str): The query string.

    Returns:
        List[str]: List of relevant document chunks.
    """
    collection = (
        create_vectorstore_collection()
    )  # Use the function to create collection
    query_embedding = encode_text(query).tolist()
    logger.debug("Performing similarity search.")
    results = query_vectorstore(
        collection=collection, query_embedding=query_embedding
    )  # Use the function to query vectorstore
    if results and "documents" in results and results["documents"]:
        logger.debug("Similarity search found relevant documents.")
        return results["documents"][0]  # Return only documents
    logger.info("Similarity search did not find relevant documents.")
    return []


@app.post("/chat/")
async def chat(chat_request: ChatRequest):
    user_query = chat_request.query
    logger.info(f"Chat query received: {user_query}")
    relevant_chunks = similarity_search_function(user_query)
    if relevant_chunks:
        logger.debug("Relevant chunks found, generating response from LLM.")
        response = phi3_llm(input_prompt=user_query, relevant_chunks=relevant_chunks)
    else:
        response = "No relevant information found in the document."
        logger.info("No relevant chunks found for the query.")
    logger.info("Chat response generated.")
    return {"response": response}


if __name__ == "__main__":
    import uvicorn

    logger.info("Starting uvicorn server.")
    uvicorn.run(app, host="0.0.0.0", port=8000)
