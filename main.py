from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import subprocess
import spacy
import pymupdf  # PyMuPDF
from collections import Counter
from transformers import pipeline

app = FastAPI(
    title="Grant Report Analysis API",
    description="API to extract key themes, impact areas, and sentiment from a PDF grant report.",
    version="1.0.0",
)

# Optionally allow CORS (if your frontend is hosted on a different domain)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load spaCy model, install if missing
MODEL_NAME = "en_core_web_sm"

try:
    nlp = spacy.load(MODEL_NAME)
except OSError:
    print(f"⚠️ Model '{MODEL_NAME}' not found. Downloading...")
    subprocess.run(["python", "-m", "spacy", "download", MODEL_NAME], check=True)
    nlp = spacy.load(MODEL_NAME)  # Reload after installation
    print(f"✅ Model '{MODEL_NAME}' installed successfully!")

# Load sentiment analysis pipeline with a specified model
sentiment_pipeline = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

def extract_text_from_pdf(file_stream):
    """Extract text from a PDF file stream using PyMuPDF."""
    doc = pymupdf.open(stream=file_stream.read(), filetype="pdf")
    text = "\n".join([page.get_text("text") for page in doc])
    return text

def preprocess_text(text: str) -> str:
    """Preprocess text: lowercasing and lemmatization, keeping only alphabetic tokens."""
    doc = nlp(text.lower())
    tokens = [token.lemma_ for token in doc if token.is_alpha]
    return " ".join(tokens)

def extract_keywords(text: str, top_n: int = 10):
    """Extract key themes (keywords) from text."""
    doc = nlp(text)
    keywords = [token.text for token in doc if token.pos_ in ["NOUN", "PROPN"]]
    return Counter(keywords).most_common(top_n)

def extract_named_entities(text: str):
    """Extract named entities (impact areas) from text."""
    doc = nlp(text)
    return [(ent.text, ent.label_) for ent in doc.ents]

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="File must be a PDF.")

    try:
        # Extract and preprocess text from the PDF
        text = extract_text_from_pdf(file.file)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {e}")

    cleaned_text = preprocess_text(text)
    key_themes = extract_keywords(cleaned_text)
    impact_areas = extract_named_entities(cleaned_text)
    # Limit to first 512 characters for sentiment analysis to avoid input size issues
    sentiment_result = sentiment_pipeline(cleaned_text[:512])
    
    return {
        "key_themes": key_themes,
        "impact_areas": impact_areas,
        "sentiment": sentiment_result,
    }
