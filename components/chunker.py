import streamlit as st
import re


def clean_text(text: str) -> str:
    """
    Basic cleanup: remove extra whitespace and normalize newlines.
    """
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 100) -> list:
    """
    Splits cleaned text into chunks with overlap.
    Stores result in session_state["chunks"].
    """
    text = clean_text(text)

    chunks = []
    start = 0
    end = chunk_size

    while start < len(text):
        chunk = text[start:end]
        chunks.append(chunk)
        start += chunk_size - overlap
        end = start + chunk_size

    st.session_state["chunks"] = chunks
    return chunks


def get_chunks_from_session() -> list:
    """
    Safely get chunks from session if they exist.
    """
    return st.session_state.get("chunks", [])
