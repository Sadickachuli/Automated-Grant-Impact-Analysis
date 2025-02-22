from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from transformers import pipeline
import spacy
import pymupdf
import os

app = FastAPI()

# CORS for Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load spaCy Model (Ensure it's Installed)
MODEL_NAME = "en_core_web_sm"
nlp = spacy.load(MODEL_NAME, disable=["parser", "tagger"])

# Sentiment Analysis Model
sentiment_pipeline = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")

def extract_text_from_pdf(file_stream, max_pages=5):
    """Extracts text from a PDF but limits to 'max_pages' to reduce memory usage."""
    doc = pymupdf.open(stream=file_stream.read(), filetype="pdf")
    text = "\n".join([doc[page].get_text("text") for page in range(min(max_pages, len(doc)))])
    return text

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="File must be a PDF.")

    try:
        text = extract_text_from_pdf(file.file)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {e}")

    sentiment_result = sentiment_pipeline(text[:512])  # Limit to 512 characters

    return {
        "sentiment": sentiment_result,
    }

# Vercel requires a handler function
def handler():
    return app
