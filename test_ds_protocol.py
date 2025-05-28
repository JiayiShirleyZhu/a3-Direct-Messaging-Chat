import ds_protocol

def test_generate_authenticate_rq():
    result = ds_protocol.generate_authenticate_rq("user1", "pass1")
    expected = '{"authenticate": {"username": "user1", "password": "pass1"}}'
    if result == expected:
        print("generate_authenticate_rq() passed")

def test_generate_directmessage_rq():
    result = ds_protocol.generate_directmessage_rq("abc123", "hi", "user2", "1234567890.0")
    expected = '{"token": "abc123", "directmessage": {"entry": "hi", "recipient": "user2", "timestamp": "1234567890.0"}}'
    if result == expected:
        print("generate_directmessage_rq() passed")

def test_generate_fetch_rq():
    result = ds_protocol.generate_fetch_rq("abc123", "unread")
    expected = '{"token": "abc123", "fetch": "unread"}'
    print("generate_fetch_rq() passed")

def test_extract_json():
    test_json = '''{"response": {"type": "ok", "message": "Welcome!", "token": "abc123", "messages": [{"from": "user2", "message": "hi", "timestamp": "1234567890.0"}]}}'''
    try:
        result = ds_protocol.extract_json(test_json)
        assert result.type == "ok"
        assert result.message == "Welcome!"
        assert result.token == "abc123"
        assert isinstance(result.messages, list)
        print("extract_json() passed")
    except Exception as e:
        print(f"failed: {e}")

if __name__ == '__main__':
    test_generate_authenticate_rq()
    test_generate_directmessage_rq()
    test_generate_fetch_rq()
    test_extract_json()