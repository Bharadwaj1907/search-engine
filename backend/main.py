from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import PyPDF2
import google.generativeai as genai
import glob
from dotenv import load_dotenv


# ---------- FastAPI Setup ----------
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- Configuration ----------
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
  # replace with your new key
genai.configure(api_key=GEMINI_API_KEY)

DOCS_DIR = "docs"
os.makedirs(DOCS_DIR, exist_ok=True)

# ---------- Helper Functions ----------
def extract_text_from_pdf(file_path):
    text = ""
    with open(file_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() or ""
    return text

def load_all_docs():
    texts = []
    for file_path in glob.glob(os.path.join(DOCS_DIR, "*")):
        if file_path.endswith(".pdf"):
            texts.append(extract_text_from_pdf(file_path))
        else:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                texts.append(f.read())
    return "\n".join(texts)

# ---------- Routes ----------
@app.post("/upload/")
async def upload_file(file: UploadFile):
    """Receive a file from frontend and save it"""
    file_path = os.path.join(DOCS_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())
    return {"message": f"{file.filename} uploaded successfully"}

class Query(BaseModel):
    question: str

@app.post("/ask/")
async def ask_question(query: Query):
    """Answer user's question based on uploaded docs"""
    documents = load_all_docs()
    if not documents.strip():
        return {"answer": "Please upload some documents first!"}

    prompt = f"Using the following documents:\n\n{documents}\n\nAnswer this question clearly:\n{query.question}"

    # ✅ Use a valid model
    model = genai.GenerativeModel("models/gemini-2.5-flash")

    # Generate response
    response = model.generate_content(prompt)

    return {"answer": response.text}
