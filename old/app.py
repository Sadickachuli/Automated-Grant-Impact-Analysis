import streamlit as st
import fitz  # PyMuPDF
import spacy
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from collections import Counter
from transformers import pipeline

# Specify the spaCy model name (installed via requirements.txt)
MODEL_NAME = "en_core_web_sm"

try:
    nlp = spacy.load(MODEL_NAME)
except OSError as e:
    st.error(f"spaCy model '{MODEL_NAME}' not found. Please ensure it is installed via requirements.txt. Error: {e}")
    st.stop()

# Load the Hugging Face sentiment analysis pipeline
sentiment_pipeline = pipeline("sentiment-analysis")

# Function to extract text from a PDF file
def extract_text_from_pdf(uploaded_file):
    with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
        text = "\n".join([page.get_text("text") for page in doc])
    return text

# Function to preprocess text
def preprocess_text(text):
    doc = nlp(text.lower())
    tokens = [token.lemma_ for token in doc if token.is_alpha]
    return " ".join(tokens)

# Function to extract key themes (keywords) from text
def extract_keywords(text, top_n=10):
    doc = nlp(text)
    keywords = [token.text for token in doc if token.pos_ in ["NOUN", "PROPN"]]
    return Counter(keywords).most_common(top_n)

# Function to extract named entities from text
def extract_named_entities(text):
    doc = nlp(text)
    return [(ent.text, ent.label_) for ent in doc.ents]

# Function to generate a word cloud from keywords
def generate_wordcloud(keywords):
    wordcloud = WordCloud(width=800, height=400, background_color="white").generate_from_frequencies(dict(keywords))
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    st.pyplot(plt)

# Function to generate a bar chart of keyword frequencies
def plot_keyword_bar_chart(keywords):
    if keywords:
        words, counts = zip(*keywords)
        plt.figure(figsize=(10, 5))
        sns.barplot(x=list(counts), y=list(words), palette="Blues_r")
        plt.xlabel("Frequency")
        plt.ylabel("Keywords")
        plt.title("Top Keywords in the Grant Report")
        st.pyplot(plt)
    else:
        st.write("No keywords found.")

# Streamlit UI
st.title("Automated Grant & Impact Analysis")
st.write("Upload a grant report to analyze key themes and impact areas.")

uploaded_file = st.file_uploader("Upload PDF", type="pdf")

if uploaded_file is not None:
    pdf_text = extract_text_from_pdf(uploaded_file)
    cleaned_text = preprocess_text(pdf_text)
    
    key_themes = extract_keywords(cleaned_text)
    impact_areas = extract_named_entities(cleaned_text)
    sentiment_result = sentiment_pipeline(cleaned_text[:512])

    st.subheader("Key Themes")
    st.write(key_themes)
    plot_keyword_bar_chart(key_themes)
    generate_wordcloud(key_themes)

    st.subheader("Impact Areas")
    st.write(impact_areas[:10])

    st.subheader("Sentiment Analysis")
    st.write(sentiment_result)
