import os
import pdfplumber
import streamlit as st

UPLOAD_DIR = "data/uploaded_pdfs"


def ensure_upload_dir():
    """Ensures the upload directory exists."""
    os.makedirs(UPLOAD_DIR, exist_ok=True)


def save_uploaded_file(uploaded_file) -> str:
    """
    Saves the uploaded file to disk and returns the full path.
    """
    ensure_upload_dir()
    file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Save file path to session
    st.session_state["pdf_path"] = file_path
    return file_path


def extract_text_from_pdf(pdf_path: str, x_tolerance: float = 1, y_tolerance: float = 1):
    """
    Extracts text from a PDF and returns a list of (Page Label, Text) tuples.
    Also saves combined text to session.
    """
    extracted_text = []

    try:
        with pdfplumber.open(pdf_path) as pdf:
            for i, page in enumerate(pdf.pages, start=1):
                try:
                    text = page.extract_text(
                        x_tolerance=x_tolerance, y_tolerance=y_tolerance)
                    if text:
                        extracted_text.append((f"Page {i}", text))
                except Exception as e:
                    st.warning(f"Error extracting text from page {i}: {e}")
    except Exception as e:
        st.error(f"Failed to open PDF: {e}")
        return None

    # Join all page texts into a single string for chunking
    full_text = "\n\n".join([text for _, text in extracted_text])

    st.session_state["pdf_text"] = full_text
    st.session_state["pdf_pages"] = extracted_text

    return extracted_text
