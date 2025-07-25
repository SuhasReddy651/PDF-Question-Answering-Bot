import streamlit as st
import os
import glob
from components.pdf_parser import save_uploaded_file, extract_text_from_pdf
from components.chunker import chunk_text
from components.vector_store import add_chunks_to_vector_store

# Page config
st.set_page_config(page_title="PDF QnA Chatbot", layout="wide")

# Hide sidebar and hamburger
st.markdown("""
    <style>
        section[data-testid="stSidebar"] { display: none !important; }
        div[data-testid="collapsedControl"] { display: none !important; }
        .main .block-container {
            padding-left: 2rem;
            padding-right: 2rem;
        }
    </style>
""", unsafe_allow_html=True)

# Title
st.title("📚 PDF QnA Chatbot")
st.markdown("""
Welcome to your AI-powered PDF assistant!  
Just upload a PDF, and start chatting with it like magic. 🧠✨
""")

# Clean up previously uploaded PDFs
UPLOAD_FOLDER = "data/uploaded_pdfs"
if os.path.exists(UPLOAD_FOLDER):
    for file in glob.glob(os.path.join(UPLOAD_FOLDER, "*.pdf")):
        try:
            os.remove(file)
        except Exception as e:
            st.warning(f"Could not remove old PDF: {e}")

# File uploader
uploaded_file = st.file_uploader("📄 Upload your PDF to begin:", type=["pdf"])

if uploaded_file:
    st.success(f"📥 Uploaded: {uploaded_file.name}")

    # Save and parse
    file_path = save_uploaded_file(uploaded_file)
    extracted_pages = extract_text_from_pdf(file_path)

    if extracted_pages:
        st.info("✅ PDF Text Extracted.")

        # Chunk and vectorize
        full_text = st.session_state.get("pdf_text", "")
        chunks = chunk_text(full_text)
        add_chunks_to_vector_store(chunks)

        # Clear previous chat and set session active
        st.session_state["chat_history"] = []
        st.session_state["chat_initialized"] = True

        # Redirect to chat page
        st.switch_page("pages/chat_page.py")
