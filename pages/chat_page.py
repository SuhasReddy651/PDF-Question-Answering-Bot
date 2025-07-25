import streamlit as st
import os
from st_chat_message import message
from components.gemini_llm import get_gemini_response
from components.vector_store import query_similar_chunks
import base64

st.set_page_config(page_title="Chat with PDF", layout="wide")
st.markdown(
    """
    <style>
        /* Hide sidebar */
        section[data-testid="stSidebar"] {
            display: none !important;
        }
        /* Hide top-left menu icon */
        div[data-testid="collapsedControl"] {
            display: none !important;
        }
        /* Expand main container to full width */
        .main .block-container {
            padding-left: 2rem;
            padding-right: 2rem;
        }
    </style>
    """,
    unsafe_allow_html=True
)
st.title("💬 Chat with your Document")

# Handle auto-end chat on page load if not explicitly redirected from upload
if "chat_initialized" not in st.session_state:
    # Clear all session state
    for key in ["chat_history", "pdf_path", "pdf_text", "pdf_pages", "chunks", "vector_index_built"]:
        st.session_state.pop(key, None)

    # Optional: delete uploaded file if present
    pdf_path = st.session_state.get("pdf_path")
    if pdf_path and os.path.exists(pdf_path):
        try:
            os.remove(pdf_path)
        except Exception:
            pass

    st.warning("Session expired or page reloaded. Redirecting to home...")
    st.switch_page("main.py")

# Handle "End Chat" button
if st.button("🔚 End Chat"):
    # Delete uploaded PDF file
    pdf_path = st.session_state.get("pdf_path")
    if pdf_path and os.path.exists(pdf_path):
        try:
            os.remove(pdf_path)
            st.success("🗑️ Uploaded PDF deleted.")
        except Exception as e:
            st.warning(f"⚠️ Failed to delete PDF: {e}")

    # Clear session state
    for key in ["chat_history", "pdf_path", "pdf_text", "pdf_pages", "chunks", "vector_index_built"]:
        st.session_state.pop(key, None)

    st.success("✅ Session ended. Returning to home...")
    st.switch_page("main.py")


if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Scrollable chat history container
with st.container():
    for chat in st.session_state.chat_history:
        message(chat["content"], is_user=chat["role"] == "user")

# Bottom-aligned input field (always rendered after history)
user_input = st.chat_input("Ask a question about the document...")

if user_input:
    message(user_input, is_user=True)
    st.session_state.chat_history.append(
        {"role": "user", "content": user_input})

    # RAG search
    similar_chunks = query_similar_chunks(user_input, top_k=3)
    context = "\n\n".join(similar_chunks)

    response = get_gemini_response(user_input, context=context)
    message(response, is_user=False)
    st.session_state.chat_history.append(
        {"role": "assistant", "content": response})
