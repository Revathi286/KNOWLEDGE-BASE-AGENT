KNOWLEDGE BASE AGENT

A lightweight, fast, and serverless RAG-free agent that allows users to:

✔ Upload a PDF, DOCX, or TXT
✔ Ask questions
✔ Get answers powered directly by Groq LLM
✔ No embeddings, no vector DB, no chunking — extremely fast


Live Demo

Demo Link:https://knowledge-base-agent-vvpkpmizybgkkslue6whze.streamlit.app/


Overview

This project implements a simple agent that takes an uploaded document, extracts all text, and uses Groq’s Llama model to answer any question using the entire content as context.

It behaves like ChatGPT with a document attached.


Features
Feature	Supported:
PDF Upload	
DOCX Upload	
TXT Upload	
Groq LLM-powered QA	
Streamlit UI	
No Vector DB	
No Chunking	
Works on Windows/Linux/Mac	


Architecture Diagram

![knowledge_base_agent_architecture](https://github.com/user-attachments/assets/4219b99b-5e9d-486d-b022-5ee18b5a4bdb)



Tech Stack

Python
FastAPI
Streamlit
Groq LLM API
pypdf, python-docx (text extraction)


Setup Instructions
1. Clone the repo
git clone https://github.com/yourname/simple-file-qa-agent
cd simple-file-qa-agent

2. Create environment
pip install -r requirements.txt

3. Add environment variables

Create .env:

GROQ_API_KEY=your_key_here
GROQ_MODEL=llama-3.1-8b-instant

4. Run Backend (FastAPI)
uvicorn simple_kb_agent:app --reload --port 8001

5. Run Frontend (Streamlit)
streamlit run kb_ui_simple.py


🚧 Limitations

Only one document stored at a time (in memory)
No conversation memory
Large PDFs may exceed Groq context limit
Not suitable for long documents (>30–40 pages)


🔮 Future Improvements

Multi-file support
Chat history
Vector embeddings option (hybrid mode)
PDF previews
Authentication (API keys)
Streaming responses
