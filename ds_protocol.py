# ds_protocol.py

# Starter code for assignment 2 in ICS 32 Programming with Software
# Libraries in Python

# Replace the following placeholders with your information.

# Jiayi Zhu
# jzhu42@uci.edu
# 94623196

"""
Defines the protocol for communicating
with the DS server using JSON format.
"""

import json
from collections import namedtuple
from typing import Union


class DSProtocolError(Exception):
    """
    Raised when there is an issue decoding
    or handling JSON protocol messages.
    """


# Create a namedtuple to hold the values we expect
# to retrieve from json messages.
ServerResponse = namedtuple(
    'ServerResponse', [
        'type', 'message', 'token', 'messages'])


def extract_json(json_msg: str) -> ServerResponse:
    """
    Parses a JSON-encoded server response into a
    ServerResponse namedtuple.

    :param json_msg: JSON string received from the server.
    :return: ServerResponse object containing response type,
    message, token, and messages.
    :raises DSProtocolError: If the JSON cannot be decoded.
    """
    try:
        json_obj = json.loads(json_msg)
        resp = json_obj.get("response", {})
        type_ = resp.get("type")
        message = resp.get("message", "")
        token = resp.get("token", None)
        messages = resp.get("messages", [])
        return ServerResponse(type_, message, token, messages)

    except Exception as exc:
        raise DSProtocolError("Json cannot be decoded.") from exc


def generate_authenticate_rq(username: str, password: str) -> str:
    """
    Generates a JSON string for authentication request.

    :param username: User's username.
    :param password: User's password.
    :return: JSON-formatted string for authentication.
    """
    return json.dumps(
        {"authenticate": {"username": username, "password": password}})


def generate_directmessage_rq(token: str,
                              message: str,
                              recipient_username: str,
                              timestamp: Union[str,
                                               float]) -> str:
    """
    Generates a JSON string for sending a direct message.

    :param token: Session token for authentication.
    :param message: Message content.
    :param recipient_username: Username of the message recipient.
    :param timestamp: Timestamp for the message.
    :return: JSON-formatted string representing the message request.
    """
    return json.dumps({"token": token,
                       "directmessage": {"entry": message,
                                         "recipient": recipient_username,
                                         "timestamp": timestamp}})


def generate_fetch_rq(token: str, fetch: str) -> str:
    """
    Generates a JSON string to fetch messages (new or all).

    :param token: Session token for authentication.
    :param fetch: Type of fetch, e.g., "new" or "all".
    :return: JSON-formatted string for fetch request.
    """
    return json.dumps({"token": token, "fetch": fetch})
