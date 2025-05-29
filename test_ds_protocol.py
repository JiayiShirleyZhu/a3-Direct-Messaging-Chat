import unittest
import ds_protocol

class TestDSProtocol(unittest.TestCase):
    def test_generate_authenticate_rq(self):
        result = ds_protocol.generate_authenticate_rq("user1", "pass1")
        expected = '{"authenticate": {"username": "user1", "password": "pass1"}}'
        self.assertEqual(result, expected)

    def test_generate_directmessage_rq(self):
        result = ds_protocol.generate_directmessage_rq("abc123", "hi", "user2", "1234567890.0")
        expected = '{"token": "abc123", "directmessage": {"entry": "hi", "recipient": "user2", "timestamp": "1234567890.0"}}'
        self.assertEqual(result, expected)

    def test_generate_fetch_rq(self):
        result = ds_protocol.generate_fetch_rq("abc123", "unread")
        expected = '{"token": "abc123", "fetch": "unread"}'
        self.assertEqual(result, expected)

    def test_extract_json(self):
        test_json = '''{
            "response": {
                "type": "ok",
                "message": "Welcome!",
                "token": "abc123",
                "messages": [{"from": "user2", "message": "hi", "timestamp": "1234567890.0"}]
            }
        }'''
        result = ds_protocol.extract_json(test_json)
        self.assertEqual(result.type, "ok")
        self.assertEqual(result.message, "Welcome!")
        self.assertEqual(result.token, "abc123")
        self.assertIsInstance(result.messages, list)
    
    def test_extract_json_invalid(self):
        invalid_json = '{"response": "missing_closing_brace"'
        with self.assertRaises(ds_protocol.DSProtocolError) as cm:
            ds_protocol.extract_json(invalid_json)
        self.assertEqual(str(cm.exception), "Json cannot be decoded.")

if __name__ == '__main__':
    unittest.main()