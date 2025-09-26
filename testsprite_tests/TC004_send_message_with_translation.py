import requests

BASE_URL = "http://localhost:5000"
TIMEOUT = 30

# Since the PRD does not specify an authentication mechanism, use the session from join_chat to preserve user context for send_message.

# We use requests.Session to maintain cookies or session context if server depends on it.
def test_send_message_with_translation():
    headers = {"Content-Type": "application/json"}

    session1 = requests.Session()
    session2 = requests.Session()

    user1 = {"username": "user1", "language": "english", "room": "testroom123"}
    user2 = {"username": "user2", "language": "spanish", "room": "testroom123"}

    # User 1 joins chat room
    resp_join_1 = session1.post(f"{BASE_URL}/join_chat", json=user1, headers=headers, timeout=TIMEOUT)
    assert resp_join_1.status_code == 200, f"User1 failed to join chat room: {resp_join_1.text}"

    # User 2 joins same chat room
    resp_join_2 = session2.post(f"{BASE_URL}/join_chat", json=user2, headers=headers, timeout=TIMEOUT)
    assert resp_join_2.status_code == 200, f"User2 failed to join chat room: {resp_join_2.text}"

    # User 1 sends a message in English
    message_content = "Hello, how are you?"
    send_msg_payload = {"content": message_content}
    resp_send = session1.post(f"{BASE_URL}/send_message", json=send_msg_payload, headers=headers, timeout=TIMEOUT)
    assert resp_send.status_code == 200, f"Send message failed: {resp_send.text}"

    message_response = resp_send.json()
    # Validate response keys and types
    assert "username" in message_response and isinstance(message_response["username"], str)
    assert "content" in message_response and isinstance(message_response["content"], str)
    assert "timestamp" in message_response and isinstance(message_response["timestamp"], str)
    assert "is_translated" in message_response and isinstance(message_response["is_translated"], bool)
    assert "is_own" in message_response and isinstance(message_response["is_own"], bool)

    # The username must match user1
    assert message_response["username"] == user1["username"]
    assert message_response["content"] == message_content
    assert message_response["is_own"] is True

    # User2 sends message
    user2_message = "¿Cómo estás?"
    resp_send_user2 = session2.post(f"{BASE_URL}/send_message", json={"content": user2_message}, headers=headers, timeout=TIMEOUT)
    assert resp_send_user2.status_code == 200, f"Send message by user2 failed: {resp_send_user2.text}"
    resp_user2_msg = resp_send_user2.json()

    assert "username" in resp_user2_msg and isinstance(resp_user2_msg["username"], str)
    assert resp_user2_msg["username"] == user2["username"]
    assert "content" in resp_user2_msg and isinstance(resp_user2_msg["content"], str)
    assert "timestamp" in resp_user2_msg and isinstance(resp_user2_msg["timestamp"], str)
    assert "is_translated" in resp_user2_msg and isinstance(resp_user2_msg["is_translated"], bool)
    assert "is_own" in resp_user2_msg and resp_user2_msg["is_own"] is True
    assert resp_user2_msg["content"] == user2_message


    # No cleanup possible without API endpoint


test_send_message_with_translation()
