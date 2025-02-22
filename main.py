import os
import subprocess
import pymupdf  # PyMuPDF for PDF extraction
from collections import Counter
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from transformers import pipeline
import spacy
import uvicorn

# Initialize FastAPI App
app = FastAPI()

# Allow CORS (so frontend can access API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load spaCy Model - Install if Missing
MODEL_NAME = "en_core_web_sm"

try:
    nlp = spacy.load(MODEL_NAME, disable=["parser", "tagger"])  # Disable unnecessary parts to save memory
except OSError:
    print(f"⚠️ Model '{MODEL_NAME}' not found. Installing...")
    subprocess.run(["python", "-m", "spacy", "download", MODEL_NAME], check=True)
    nlp = spacy.load(MODEL_NAME, disable=["parser", "tagger"])  # Reload after install
    print(f"✅ Model '{MODEL_NAME}' installed and loaded!")

# Load Sentiment Analysis Model (Using a Smaller Model)
sentiment_pipeline = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")

def extract_text_from_pdf(file_stream, max_pages=5):
    """
    Extracts text from a PDF but limits to 'max_pages' to reduce memory usage.
    """
    doc = pymupdf.open(stream=file_stream.read(), filetype="pdf")
    text = "\n".join([doc[page].get_text("text") for page in range(min(max_pages, len(doc)))])
    return text

def preprocess_text(text: str) -> str:
    """
    Lowercases, lemmatizes, and removes non-alphabetic words to clean text.
    """
    doc = nlp(text.lower())
    tokens = [token.lemma_ for token in doc if token.is_alpha]
    return " ".join(tokens)

def extract_keywords(text: str, top_n: int = 10):
    """
    Extracts key themes (keywords) using NLP.
    """
    doc = nlp(text)
    keywords = [token.text for token in doc if token.pos_ in ["NOUN", "PROPN"]]
    return Counter(keywords).most_common(top_n)

def extract_named_entities(text: str):
    """
    Extracts named entities (impact areas) using NLP.
    """
    doc = nlp(text)
    return [(ent.text, ent.label_) for ent in doc.ents]

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="File must be a PDF.")

    try:
        text = extract_text_from_pdf(file.file)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {e}")

    cleaned_text = preprocess_text(text)
    key_themes = extract_keywords(cleaned_text)
    impact_areas = extract_named_entities(cleaned_text)
    sentiment_result = sentiment_pipeline(cleaned_text[:512])  # Limit characters to avoid memory issues

    return {
        "key_themes": key_themes,
        "impact_areas": impact_areas,
        "sentiment": sentiment_result,
    }

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))  # Get PORT from environment, default to 8000
    uvicorn.run(app, host="0.0.0.0", port=port)
