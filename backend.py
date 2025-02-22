# backend.py
from flask import Flask, request, jsonify
import io
import fitz  # PyMuPDF
import spacy
from collections import Counter
from transformers import pipeline

app = Flask(__name__)

# Load spaCy model and sentiment analysis pipeline
MODEL_NAME = "en_core_web_sm"
nlp = spacy.load(MODEL_NAME)
sentiment_pipeline = pipeline("sentiment-analysis")

def extract_text_from_pdf(file_stream):
    # Open the PDF from the file stream
    doc = fitz.open(stream=file_stream.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text("text") + "\n"
    return text

def preprocess_text(text):
    # Lowercase and lemmatize text while filtering out non-alphabetic tokens
    doc = nlp(text.lower())
    tokens = [token.lemma_ for token in doc if token.is_alpha]
    return " ".join(tokens)

def extract_keywords(text, top_n=10):
    doc = nlp(text)
    keywords = [token.text for token in doc if token.pos_ in ["NOUN", "PROPN"]]
    return Counter(keywords).most_common(top_n)

def extract_named_entities(text):
    doc = nlp(text)
    return [(ent.text, ent.label_) for ent in doc.ents]

@app.route("/analyze", methods=["POST"])
def analyze():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400
    file = request.files["file"]
    
    # Extract and preprocess text
    text = extract_text_from_pdf(file)
    cleaned_text = preprocess_text(text)
    
    # Get analysis results
    key_themes = extract_keywords(cleaned_text)
    impact_areas = extract_named_entities(cleaned_text)
    # Use only the first 512 characters for sentiment analysis to avoid input size limits
    sentiment_result = sentiment_pipeline(cleaned_text[:512])
    
    return jsonify({
        "key_themes": key_themes,
        "impact_areas": impact_areas,
        "sentiment": sentiment_result
    })

if __name__ == "__main__":
    app.run(debug=True)
