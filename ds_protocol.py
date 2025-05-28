# ds_protocol.py

# Starter code for assignment 2 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# Jiayi Zhu
# jzhu42@uci.edu
# 94623196
import json
from collections import namedtuple

class DSProtocolError(Exception):
  pass

# Create a namedtuple to hold the values we expect to retrieve from json messages.
ServerResponse = namedtuple('ServerResponse', ['type', 'message', 'token', 'messages'])

def extract_json(json_msg:str) -> ServerResponse:
  '''
  Call the json.loads function on a json string and convert it to a DataTuple object
  '''
  try:
    json_obj = json.loads(json_msg)
    resp = json_obj.get("response", {})
    type_ = resp.get("type")
    message = resp.get("message", "")
    token = resp.get("token", None)
    messages = resp.get("messages", [])
    return ServerResponse(type_, message, token, messages)
  
  except json.JSONDecodeError:
    raise DSProtocolError("Json cannot be decoded.")

def generate_authenticate_rq(username, password):
  return json.dumps({"authenticate": {"username": username,"password": password}})

def generate_directmessage_rq(token, message, recepient_username, timestamp):
  return json.dumps({"token": token, "directmessage": {"entry": message,"recipient": recepient_username, "timestamp": timestamp}})

def generate_fetch_rq(token, fetch):
  return json.dumps({"token": token, "fetch": fetch})

