# app/components/vector_store.py

import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
import streamlit as st

# Setup embedding model
embedding_fn = SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2")

# Setup persistent Chroma client (optional path)
client = chromadb.Client()
collection = client.get_or_create_collection(
    name="pdf_chunks",
    embedding_function=embedding_fn
)


def add_chunks_to_vector_store(chunks: list):
    """
    Adds the chunked text to the Chroma vector database.
    Stores IDs as id_0, id_1, ..., etc.
    """
    ids = [f"id_{i}" for i in range(len(chunks))]

    # Clear old entries (only if any exist)
    existing = collection.get()
    if existing and existing.get("ids"):
        collection.delete(ids=existing["ids"])

    # Add new chunk vectors
    collection.add(
        documents=chunks,
        ids=ids
    )

    st.session_state["vector_index_built"] = True
    st.success(f"✅ {len(chunks)} chunks indexed into ChromaDB.")


def query_similar_chunks(query: str, top_k: int = 3) -> list:
    """
    Retrieves the top-K most relevant chunks to the query.
    """
    result = collection.query(
        query_texts=[query],
        n_results=top_k
    )

    return result["documents"][0] if result["documents"] else []
