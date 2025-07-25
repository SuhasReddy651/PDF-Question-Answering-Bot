# 📄 PDF Question Answering Bot

An interactive QnA chatbot that allows users to upload PDF documents, parse content, and query the text using Google Gemini Pro via a conversational interface built with Streamlit.

---

## 🚀 Features

- 📄 Upload and parse PDF files.
- 🔍 Intelligent chunking for improved question matching.
- 📚 Vector-based semantic search using ChromaDB.
- 🤖 LLM-powered QnA system using `google-genai`.
- 🖥️ Streamlit-based intuitive frontend.

---

## 🗂️ Project Structure

```
PDF-QnA-Bot/
├── components/
│   ├── chunker.py           # Splits PDF content into manageable chunks
│   ├── gemini_llm.py        # Sends user query + context to Gemini LLM
│   ├── pdf_parser.py        # Extracts text from PDF using PyPDF2
│   └── vector_store.py      # Embeds and stores text chunks using ChromaDB
├── data/
│   └── uploaded_pdfs/       # Stores user-uploaded PDFs
├── pages/
│   └── chat_page.py         # Streamlit page for chat interaction
├── main.py                  # Streamlit app entry point
├── requirements.txt         # Python dependencies
└── README.md                # This file
```

---

## ⚙️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/PDF-QnA-Bot.git
cd PDF-QnA-Bot
```

### 2. Set up a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate  # Mac/Linux
.venv\Scripts\activate     # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

> If using Google Colab or Jupyter:
>
> ```python
> !pip install -q -U google-genai
> ```

---

## 🔐 Environment Variables

Create a `.env` file in the project root and add your Gemini API key:

```env
GOOGLE_API_KEY=your_google_genai_key_here
```

---

## 🧠 How It Works

1. **Upload** a PDF → Stored in `data/uploaded_pdfs/`.
2. **Extract** the text using `pdf_parser.py`.
3. **Chunk** the text using `chunker.py` for better semantic relevance.
4. **Embed** and **store** using `vector_store.py` + ChromaDB.
5. **Query** using `gemini_llm.py` with context retrieved by similarity search.
6. **Chat** with results shown via the `chat_page.py` interface in Streamlit.

---

## 🧩 Tech Stack

- **Frontend:** Streamlit
- **PDF Parsing:** PyPDF2
- **Vector DB:** ChromaDB
- **LLM:** Google Gemini via `google-genai`
- **Env Management:** python-dotenv

---

## ✅ To Run

```bash
streamlit run main.py
```

---

## 💡 Future Additions

- Multi-document knowledge querying
- Chat history and memory
- Export chat transcripts
- Speech-based query input

---

## 📜 License

MIT License © 2025 Surya Suhas Reddy Sathi
