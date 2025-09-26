import requests

def test_get_main_chat_page():
    base_url = "http://localhost:5000"
    url = f"{base_url}/"
    headers = {
        "Accept": "text/html"
    }

    try:
        response = requests.get(url, headers=headers, timeout=30)
    except requests.RequestException as e:
        assert False, f"Request to get main chat page failed: {e}"

    assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}"
    content_type = response.headers.get("Content-Type", "")
    assert "text/html" in content_type, f"Expected Content-Type to be text/html but got {content_type}"
    assert len(response.text) > 0, "Response HTML content is empty"

test_get_main_chat_page()