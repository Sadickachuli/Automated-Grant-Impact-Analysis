import pytest
from app import extract_text_from_pdf, preprocess_text, extract_keywords, extract_named_entities

# Sample text for testing
sample_text = """
The USAID grant focuses on education, healthcare, and sustainability.
Organizations such as UNICEF and WHO are involved.
Funding is provided to rural communities for better infrastructure.
"""

def test_preprocess_text():
    processed = preprocess_text(sample_text)
    assert isinstance(processed, str)
    assert len(processed) > 0

def test_extract_keywords():
    keywords = extract_keywords(sample_text, top_n=5)
    assert isinstance(keywords, list)
    assert len(keywords) == 5
    assert all(isinstance(i, tuple) and isinstance(i[0], str) and isinstance(i[1], int) for i in keywords)

def test_extract_named_entities():
    entities = extract_named_entities(sample_text)
    assert isinstance(entities, list)
    assert all(isinstance(i, tuple) and len(i) == 2 for i in entities)

if __name__ == "__main__":
    pytest.main()
