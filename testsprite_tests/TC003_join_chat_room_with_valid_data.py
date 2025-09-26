import requests

BASE_URL = "http://localhost:5000"
TIMEOUT = 30
HEADERS = {"Content-Type": "application/json"}

def test_join_chat_room_with_valid_data():
    url = f"{BASE_URL}/join_chat"
    payload = {
        "username": "testuser123",
        "language": "en",
        "room": "general"
    }
    try:
        response = requests.post(url, json=payload, headers=HEADERS, timeout=TIMEOUT)
        assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}"
    except requests.exceptions.RequestException as e:
        assert False, f"Request to join chat room failed: {str(e)}"

test_join_chat_room_with_valid_data()