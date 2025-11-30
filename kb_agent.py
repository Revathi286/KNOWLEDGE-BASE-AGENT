# simple_kb_agent.py  (Windows-compatible + No Chunks)

import os
import tempfile
from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
import uvicorn
from pypdf import PdfReader
import docx
from groq import Groq

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")

if not GROQ_API_KEY:
    raise SystemExit("Please set GROQ_API_KEY in .env")

app = FastAPI(title="KNOWLEDGE BASE AGENT")

groq_client = Groq(api_key=GROQ_API_KEY)

# In-memory document store
DOCUMENT_TEXT = ""


# ---------- EXTRACT TEXT ----------
def extract_pdf(path: str) -> str:
    try:
        reader = PdfReader(path)
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    except:
        return ""


def extract_docx_file(path: str) -> str:
    try:
        doc = docx.Document(path)
        return "\n".join(p.text for p in doc.paragraphs)
    except:
        return ""


# ---------- UPLOAD ----------
@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    global DOCUMENT_TEXT

    # Cross-platform temp directory (Windows safe)
    temp_dir = tempfile.gettempdir()
    temp_path = os.path.join(temp_dir, file.filename)

    # Save uploaded file
    with open(temp_path, "wb") as f:
        f.write(await file.read())

    fname = file.filename.lower()

    # Extract text based on file extension
    if fname.endswith(".pdf"):
        DOCUMENT_TEXT = extract_pdf(temp_path)
    elif fname.endswith(".docx") or fname.endswith(".doc"):
        DOCUMENT_TEXT = extract_docx_file(temp_path)
    else:
        DOCUMENT_TEXT = open(temp_path, "r", encoding="utf8", errors="ignore").read()

    # Cleanup
    if os.path.exists(temp_path):
        os.remove(temp_path)

    if not DOCUMENT_TEXT.strip():
        raise HTTPException(status_code=400, detail="Unable to extract text from file")

    return {
        "status": "uploaded",
        "characters": len(DOCUMENT_TEXT),
        "message": "File uploaded successfully. You can now ask questions."
    }


# ---------- ASK ----------
@app.post("/ask")
async def ask(q: str = Form(...)):
    if not DOCUMENT_TEXT.strip():
        raise HTTPException(status_code=400, detail="No file uploaded yet")

    prompt = f"""
Use ONLY the document content below to answer the question.

DOCUMENT:
---------------------
{DOCUMENT_TEXT}
---------------------

QUESTION: {q}

Answer clearly using only the above document.
"""

    try:
        resp = groq_client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=800,
            temperature=0
        )

        answer = resp.choices[0].message.content
        return {"answer": answer}

    except Exception as e:
        return JSONResponse({"error": "Groq error", "details": str(e)}, status_code=500)


@app.get("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run("simple_kb_agent:app", host="0.0.0.0", port=8001, reload=True)
