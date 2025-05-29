# ds_messenger.py

# Starter code for assignment 2 in ICS 32
# Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# Jiayi Zhu
# jzhu42@uci.edu
# 94623196

"""
Module for handling direct messaging client operations using a DS server.
"""
import socket
import time
import ds_protocol

# pylint: disable=too-few-public-methods


class DirectMessage:
    """Represents a direct message object."""

    def __init__(self) -> None:
        """
        Represents a direct message exchanged between users.
        """
        self.recipient = None
        self.message = None
        self.sender = None
        self.timestamp = None

# pylint: disable=too-many-instance-attributes


class DirectMessenger:
    """
    Handles sending and receiving direct messages to/from the DS server.
    """

    def __init__(
            self,
            dsuserver: str = None,
            username: str = None,
            password: str = None):
        """
        Initializes the messenger, connects to the server, and authenticates
        the user.

        :param dsuserver: The address of the DS server.
        :param username: The username to authenticate with.
        :param password: The password to authenticate with.
        """
        self.dsuserver = dsuserver
        self.username = username
        self.password = password
        self.token = None
        self.port = 3001

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.dsuserver, self.port))
        self.sendfile = self.client.makefile('w')
        self.recvfile = self.client.makefile('r')

        self._authenticate()

    def _authenticate(self) -> None:
        """
        Sends authentication request to the server
        and stores the session token.

        :raises Exception: If authentication fails.
        """
        json_msg = ds_protocol.generate_authenticate_rq(
            self.username, self.password)
        self.sendfile.write(json_msg + '\r\n')
        self.sendfile.flush()

        response = self.recvfile.readline()
        parsed = ds_protocol.extract_json(response)

        if parsed.type == 'ok':
            self.token = parsed.token
        else:
            raise ValueError(f"Authentication failed: {parsed.message}")

    def send(self, message: str, recipient: str) -> bool:
        """
        Sends a message to a specified recipient.

        :param message: The content of the message to send.
        :param recipient: The recipient's username.
        :return: True if the message was sent successfully, False otherwise.
        """
        try:
            timestamp = time.time()
            json_msg = ds_protocol.generate_directmessage_rq(
                self.token, message, recipient, timestamp)
            self.sendfile.write(json_msg + '\r\n')
            self.sendfile.flush()

            response = self.recvfile.readline()
            parsed = ds_protocol.extract_json(response)

            return parsed.type == "ok"

        except Exception:  # pylint: disable=broad-exception-caught
            return False

    def retrieve_new(self) -> list:
        """
        Retrieves new/unread messages from the server.

        :return: A list of DirectMessage objects.
        """
        messages = []
        msg = ds_protocol.generate_fetch_rq(self.token, "unread")
        self.sendfile.write(msg + '\r\n')
        self.sendfile.flush()

        response = self.recvfile.readline()
        parsed = ds_protocol.extract_json(response)

        if parsed.type == "ok":
            for m in parsed.messages:
                dm = DirectMessage()
                dm.message = m.get("message")
                dm.timestamp = m.get("timestamp")
                if "from" in m:
                    dm.sender = m["from"]
                    dm.recipient = self.username
                elif "recipient" in m:
                    dm.sender = self.username
                    dm.recipient = m["recipient"]
                messages.append(dm)

        return messages

    def retrieve_all(self) -> list:
        """
        Retrieves all messages from the server.

        :return: A list of DirectMessage objects.
        """
        messages = []
        msg = ds_protocol.generate_fetch_rq(self.token, "all")
        self.sendfile.write(msg + '\r\n')
        self.sendfile.flush()

        response = self.recvfile.readline()
        parsed = ds_protocol.extract_json(response)

        if parsed.type == "ok":
            for m in parsed.messages:
                dm = DirectMessage()
                dm.message = m.get("message")
                dm.timestamp = m.get("timestamp")
                if "from" in m:
                    dm.sender = m["from"]
                    dm.recipient = self.username
                elif "recipient" in m:
                    dm.sender = self.username
                    dm.recipient = m["recipient"]
                messages.append(dm)

        return messages

    def close(self) -> None:
        """
        Closes the connection to the server and all open file streams.
        """
        self.sendfile.close()
        self.recvfile.close()
        self.client.close()
