# kb_ui_simple.py  (Updated for simple_kb_agent.py)
import streamlit as st
import requests

st.set_page_config(page_title="KNOWLEDGE BASE AGENT", layout="centered")
st.title(" KNOWLEDGE BASE AGENT")

API = st.text_input("API base URL", "http://localhost:8001")

# --------------------------
# 1. Upload File
# --------------------------
st.markdown("## 1. Upload a File (PDF / DOCX / TXT)")
uploaded = st.file_uploader("Upload file", type=["pdf", "docx", "txt"])

if uploaded and st.button("Upload"):
    files = {"file": (uploaded.name, uploaded.getvalue())}
    try:
        r = requests.post(f"{API}/upload", files=files, timeout=200)
    except Exception as e:
        st.error(f"Request error: {e}")
    else:
        st.write("Status:", r.status_code)
        try:
            st.json(r.json())
        except Exception:
            st.text(r.text)

# --------------------------
# 2. Ask a Question
# --------------------------
st.markdown("---")
st.markdown("## 2. Ask a Question About the Uploaded File")

q = st.text_input("Enter your question")

if st.button("Ask"):
    if not q.strip():
        st.warning("Please enter a question.")
    else:
        try:
            r = requests.post(f"{API}/ask", data={"q": q}, timeout=200)
        except Exception as e:
            st.error(f"Request error: {e}")
        else:
            st.write("Status:", r.status_code)
            if r.ok:
                try:
                    out = r.json()
                    st.subheader("Answer")
                    st.write(out.get("answer", ""))
                except Exception:
                    st.text("Server did not return JSON:")
                    st.text(r.text)
            else:
                st.error("Query failed")
                st.text(r.text)

# --------------------------
# 3. Health Check
# --------------------------
st.markdown("---")
if st.button("Check API Health"):
    try:
        r = requests.get(f"{API}/health", timeout=10)
        st.json(r.json())
    except Exception as e:
        st.error(f"Health check error: {e}")
