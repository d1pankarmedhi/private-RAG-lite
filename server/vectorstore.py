__import__("pysqlite3")
import sys

from log_utils import logger

sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")
from collections import defaultdict
from typing import List, Optional

import chromadb
from chromadb import Collection
from config import COLLECTION_NAME


class ChromaStore:
    def __init__(
        self,
        collection_name: str,
        storage_path: str = "./chroma",
        database: str = "database",
        metadata: dict = {"hnsw:space": "cosine"},
    ) -> None:
        """Initiate Chromadb
        - collection_name(str): name of the collection
        - metadata(dict): available options for 'hnsw:space' are 'l2', 'ip' or 'cosine'.
        """

        self.collection_name = collection_name
        self.metadata = metadata
        self.storage_path = storage_path
        self.database = database

        self.client = chromadb.PersistentClient(path=self.storage_path)

    def _health_check(self) -> bool:
        return isinstance(self.client.heartbeat(), int)

    def create(self):
        collection = self.client.get_or_create_collection(
            name=self.collection_name,
        )
        return collection

    def add(
        self,
        collection: Collection,
        embeddings: List[float],
        documents: List[str],
        ids: List[str],
    ):
        """Add embeddings, documents to index or collection.

        Args:
        - collection: created collection.
        - embeddings: list of embeddings
        - documents: text documents
        - ids: list of ids"""
        try:
            collection.add(
                embeddings=embeddings,
                ids=ids,
                documents=documents,
            )
        except Exception as e:
            raise Exception(f"Failed to add documents to Chroma store. {e}")

    def query(
        self,
        collection: Collection,
        query_embedding: List[float],
        top_k: int = 3,
    ) -> list:
        """Retrieve relevant images from chroma database.

        Args:
        - collection: created collection.
        - query_embedding: query image embedding.
        - top_k (int): top k images to retrieve.

        Returns:
        - list of images along with their score.
        """
        result = collection.query(query_embeddings=query_embedding, n_results=top_k)
        relevant_chunks = [chunk for chunk in result["documents"][0]]
        return relevant_chunks
        # scores = [round(score, 3) for score in result["distances"][0]]
        # return list(zip(relevant_chunks, scores))

    def delete(self, collection_name: str):
        try:
            self.client.delete_collection(collection_name)
            return True
        except Exception as e:
            raise Exception("Failed to delete collection", e)

    def list_collections(self):
        return self.client.list_collections()

    @staticmethod
    def collection_info(collection: Collection):
        info = defaultdict(str)
        info["count"] = collection.count()
        info["top_10_items"] = collection.peek()
        return info


def create_vectorstore_collection():
    """
    Creates and returns a ChromaDB collection.

    Returns:
        chromadb.api.models.Collection.Collection: ChromaDB collection object.
    """
    chromastore = ChromaStore(collection_name=COLLECTION_NAME)
    logger.info(f"Creating ChromaDB collection: {COLLECTION_NAME}")
    return chromastore.create()


def delete_vectorstore_collection():
    """
    Deletes the ChromaDB collection if it exists.
    """
    chromastore = ChromaStore(collection_name=COLLECTION_NAME)
    if COLLECTION_NAME in chromastore.list_collections():
        chromastore.delete(COLLECTION_NAME)
        logger.info(f"Old database collection '{COLLECTION_NAME}' cleaned!")
    else:
        logger.info(f"No database collection '{COLLECTION_NAME}' found to delete.")


def add_to_vectorstore(
    collection,
    embeddings: List[List[float]],
    documents: List[str],
    ids: List[str],
    doc_id: Optional[str] = None,
):
    """
    Adds data to the ChromaDB vector store, now including document ID.

    Args:
        collection: ChromaDB collection object.
        embeddings (List[List[float]]): List of embeddings.
        documents (List[str]): List of document texts.
        ids (List[str]): List of unique IDs for chunks.
        doc_id (Optional[str]): Unique ID for the document (optional).
    """
    chromastore = ChromaStore(collection_name=COLLECTION_NAME)
    metadatas = []  # Prepare metadata list
    for _ in documents:  # Create metadata for each document chunk
        metadata = {}
        if doc_id:
            metadata["document_id"] = doc_id  # Add document ID to metadata
        metadatas.append(metadata)

    logger.debug(f"Adding {len(documents)} documents to vectorstore.")
    chromastore.add(
        collection=collection,
        embeddings=embeddings,
        documents=documents,
        ids=ids,
        metadatas=metadatas,
    )
    logger.info("Document chunks successfully added to vectorstore")


def query_vectorstore(collection, query_embedding: List[float]):
    """
    Performs similarity search in the ChromaDB vector store.

    Args:
        collection: ChromaDB collection object.
        query_embedding (List[float]): Embedding of the query.

    Returns:
        dict: Search results from ChromaDB.
    """
    chromastore = ChromaStore(collection_name=COLLECTION_NAME)
    logger.debug("Performing similarity search in vectorstore.")
    return chromastore.query(collection=collection, query_embedding=query_embedding)
