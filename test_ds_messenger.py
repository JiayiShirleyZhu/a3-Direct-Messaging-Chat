"""Unit tests for the ds_messenger module."""

import json
import unittest
from unittest.mock import patch, MagicMock
from ds_messenger import DirectMessage, DirectMessenger

SERVER = "127.0.0.1"
USERNAME = "Shirley"
PASSWORD = "password"
RECIPIENT = "Emily"


class TestDirectMessenger(unittest.TestCase):
    """Tests for the DirectMessenger class."""
    def test_direct_message_attributes(self):
        """Test that DirectMessage initializes with correct attributes."""
        dm = DirectMessage()
        dm.recipient = "Emily"
        dm.message = "Hello"
        dm.sender = "Shirley"
        dm.timestamp = "1234567890.0"

        self.assertEqual(dm.recipient, "Emily")
        self.assertEqual(dm.message, "Hello")
        self.assertEqual(dm.sender, "Shirley")
        self.assertEqual(dm.timestamp, "1234567890.0")

    def setUp(self):
        """Connect to the server once before each test"""
        self.dm = DirectMessenger(SERVER, USERNAME, PASSWORD)

    def test_send(self):
        """Test sending a message returns True or False"""
        result = self.dm.send("hello from unittest!", RECIPIENT)
        self.assertIsInstance(result, bool)

    def test_retrieve_new(self):
        """
        Test retrieving new messages returns a
        list of messages with expected attributes
        """
        messages = self.dm.retrieve_new()
        self.assertIsInstance(messages, list)
        for m in messages:
            self.assertTrue(hasattr(m, 'message'))
            self.assertTrue(hasattr(m, 'sender'))
            self.assertTrue(hasattr(m, 'timestamp'))

    def test_retrieve_all(self):
        """Test retrieving all messages returns a list of messages"""
        messages = self.dm.retrieve_all()
        self.assertIsInstance(messages, list)
        for m in messages:
            self.assertTrue(hasattr(m, 'message'))
            self.assertTrue(hasattr(m, 'timestamp'))
            self.assertTrue(hasattr(m, 'sender') or hasattr(m, 'recipient'))

    def test_retrieve_new_from_field(self):
        """Covers 'from' in message dict"""
        fake_response = {
            "response": {
                "type": "ok",
                "messages": [
                    {
                        "from": "Alice",
                        "message": "hi from Alice",
                        "timestamp": "111.0"
                    }
                ]
            }
        }
        self.dm.recvfile.readline = MagicMock(
            return_value=json.dumps(fake_response) + '\r\n')
        result = self.dm.retrieve_new()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].sender, "Alice")
        self.assertEqual(result[0].recipient, self.dm.username)

    def test_retrieve_new_recipient_field(self):
        """Covers 'recipient' in message dict"""
        fake_response = {
            "response": {
                "type": "ok",
                "messages": [
                    {
                        "recipient": "Bob",
                        "message": "hi to Bob",
                        "timestamp": "112.0"
                    }
                ]
            }
        }
        self.dm.recvfile.readline = MagicMock(
            return_value=json.dumps(fake_response) + '\r\n')
        result = self.dm.retrieve_new()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].sender, self.dm.username)
        self.assertEqual(result[0].recipient, "Bob")

    def test_retrieve_all_from_field(self):
        """Covers 'from' in message dict"""
        fake_response = {
            "response": {
                "type": "ok",
                "messages": [
                    {
                        "from": "Alice",
                        "message": "hi from Alice",
                        "timestamp": "111.0"
                    }
                ]
            }
        }
        self.dm.recvfile.readline = MagicMock(
            return_value=json.dumps(fake_response) + '\r\n')
        result = self.dm.retrieve_all()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].sender, "Alice")
        self.assertEqual(result[0].recipient, self.dm.username)

    def test_retrieve_all_recipient_field(self):
        """Covers 'recipient' in message dict"""
        fake_response = {
            "response": {
                "type": "ok",
                "messages": [
                    {
                        "recipient": "Bob",
                        "message": "hi to Bob",
                        "timestamp": "112.0"
                    }
                ]
            }
        }
        self.dm.recvfile.readline = MagicMock(
            return_value=json.dumps(fake_response) + '\r\n')
        result = self.dm.retrieve_all()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].sender, self.dm.username)
        self.assertEqual(result[0].recipient, "Bob")

    def test_send_returns_true(self):
        """Ensure send() hits the return True path"""
        with patch('ds_messenger.socket.socket') as mock_socket:
            mock_client = MagicMock()
            mock_socket.return_value = mock_client

            mock_sendfile = MagicMock()
            mock_recvfile = MagicMock()
            mock_recvfile.readline.side_effect = [
                '{"response": {"type": "ok", "token": "abc"}}\r\n',  # auth
                '{"response": {"type": "ok", "message": "sent"}}\r\n'  # send
            ]
            mock_client.makefile.side_effect = [mock_sendfile, mock_recvfile]

            dm = DirectMessenger("127.0.0.1", "user", "pass")
            result = dm.send("hi", "someone")
            assert result is True

    def test_send_json_decode_error(self):
        """Covers send() when JSON is invalid and raises exception"""
        self.dm.recvfile.readline = lambda: "INVALID_JSON\r\n"
        result = self.dm.send("trigger error", RECIPIENT)
        self.assertFalse(result)

    def test_authentication_failure(self):
        """Covers raise Exception if authentication fails"""

        with patch('ds_messenger.socket.socket') as mock_socket:
            mock_client = MagicMock()
            mock_socket.return_value = mock_client

            mock_sendfile = MagicMock()
            mock_recvfile = MagicMock()

            mock_recvfile.readline.return_value = (
                '{"response": {"type": "error", "message": "fail"}}\r\n'
            )
            mock_client.makefile.side_effect = [mock_sendfile, mock_recvfile]

            with self.assertRaises(Exception) as context:
                DirectMessenger("127.0.0.1", "fake_user", "fake_pass")

            self.assertIn("Authentication failed", str(context.exception))

    def tearDown(self):
        """Close socket after each test"""
        if self.dm:
            self.dm.close()


if __name__ == '__main__':
    unittest.main()
