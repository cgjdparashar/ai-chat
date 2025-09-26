import requests

BASE_URL = "http://localhost:5000"
TIMEOUT = 30
HEADERS = {"Content-Type": "application/json"}

def test_translate_text_using_ollama_api():
    url = f"{BASE_URL}/translate"

    # Test valid translation request
    payload_valid = {
        "text": "Hello, world!",
        "source_language": "en",
        "target_language": "es"
    }
    try:
        response = requests.post(url, json=payload_valid, headers=HEADERS, timeout=TIMEOUT)
        assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}"
        data = response.json()
        assert "translated_text" in data, "Response JSON missing 'translated_text'"
        assert isinstance(data["translated_text"], str), "'translated_text' should be a string"
        assert len(data["translated_text"]) > 0, "'translated_text' should not be empty"
    except requests.RequestException as e:
        assert False, f"Request failed: {e}"

    # Test missing required fields (no text)
    payload_missing_text = {
        "target_language": "fr"
    }
    try:
        response = requests.post(url, json=payload_missing_text, headers=HEADERS, timeout=TIMEOUT)
        # Expecting error status code, could be 400 or 422 depending on API error handling
        assert response.status_code >= 400, f"Expected client error for missing text, got {response.status_code}"
    except requests.RequestException as e:
        # If network error, fail the test
        assert False, f"Request failed: {e}"

    # Test invalid target language
    payload_invalid_lang = {
        "text": "Hello",
        "target_language": "invalid-lang-code"
    }
    try:
        response = requests.post(url, json=payload_invalid_lang, headers=HEADERS, timeout=TIMEOUT)
        assert response.status_code == 200, f"Expected 200 OK for invalid target language, got {response.status_code}"
        data = response.json()
        assert "translated_text" in data, "Response JSON missing 'translated_text' for invalid target language"
        assert isinstance(data["translated_text"], str), "'translated_text' should be a string for invalid target language"
    except requests.RequestException as e:
        assert False, f"Request failed: {e}"

    # Test auto-detection of source language (no source_language field)
    payload_auto_source = {
        "text": "Bonjour",
        "target_language": "en"
    }
    try:
        response = requests.post(url, json=payload_auto_source, headers=HEADERS, timeout=TIMEOUT)
        assert response.status_code == 200, f"Expected 200 OK for auto-detect, got {response.status_code}"
        data = response.json()
        assert "translated_text" in data, "Response JSON missing 'translated_text' for auto-detect"
        assert isinstance(data["translated_text"], str), "'translated_text' should be a string for auto-detect"
        assert len(data["translated_text"]) > 0, "'translated_text' should not be empty for auto-detect"
    except requests.RequestException as e:
        assert False, f"Request failed: {e}"

test_translate_text_using_ollama_api()
