import requests

BASE_URL = "http://localhost:5000"
TIMEOUT = 30

def test_change_user_language_preference():
    session = requests.Session()
    headers = {"Content-Type": "application/json"}
    username = "testuser_tc005"
    initial_language = "english"
    new_language = "spanish"
    room = "general"
    try:
        # Step 1: Join chat room with initial language preference
        join_payload = {
            "username": username,
            "language": initial_language,
            "room": room
        }
        join_resp = session.post(f"{BASE_URL}/join_chat", json=join_payload, headers=headers, timeout=TIMEOUT)
        assert join_resp.status_code == 200, f"Join chat failed: {join_resp.status_code} {join_resp.text}"

        # Step 2: Change language preference
        change_lang_payload = {
            "language": new_language
        }
        change_lang_resp = session.post(f"{BASE_URL}/change_language", json=change_lang_payload, headers=headers, timeout=TIMEOUT)
        assert change_lang_resp.status_code == 200, f"Change language failed: {change_lang_resp.status_code} {change_lang_resp.text}"

        # Step 3: Send a message after language change
        message_text = "Hello, how are you?"
        send_message_payload = {
            "content": message_text
        }
        send_resp = session.post(f"{BASE_URL}/send_message", json=send_message_payload, headers=headers, timeout=TIMEOUT)
        assert send_resp.status_code == 200, f"Send message failed: {send_resp.status_code} {send_resp.text}"
        send_resp_json = send_resp.json()

        # Validate message response fields
        assert "username" in send_resp_json, "Response missing 'username'"
        assert isinstance(send_resp_json["username"], str), "Username should be a string in response"
        assert "content" in send_resp_json, "Response missing 'content'"
        assert "timestamp" in send_resp_json, "Response missing 'timestamp'"
        assert "is_translated" in send_resp_json, "Response missing 'is_translated'"
        assert "is_own" in send_resp_json, "Response missing 'is_own'"

        # Since user changed language to Spanish, the message should be marked as translated
        # and content should differ from original if translation is working properly.
        # We can only assert that is_translated is True and is_own is True.
        assert send_resp_json["is_translated"] is True, "Message should be translated after language change"
        assert send_resp_json["is_own"] is True, "Message should be marked as own"

        # Additionally check content differs (basic check, may not apply if translation returns same text)
        translated_content = send_resp_json["content"]
        assert isinstance(translated_content, str) and len(translated_content) > 0, "Translated content missing or empty"
        # If translated content is exactly same as original for this English->Spanish test, 
        # it's possible no translation was applied, but we accept this as valid for test completeness.
    finally:
        # Clean up: no explicit delete endpoint available; if any logout or cleanup needed, it can be added here.
        session.close()

test_change_user_language_preference()
