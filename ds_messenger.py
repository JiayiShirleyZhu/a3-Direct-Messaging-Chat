# ds_messenger.py

# Starter code for assignment 2 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# Jiayi Zhu
# jzhu42@uci.edu
# 94623196
import socket
import time
import ds_protocol

class DirectMessage:
  def __init__(self):
    self.recipient = None
    self.message = None
    self.sender = None
    self.timestamp = None

class DirectMessenger:
  def __init__(self, dsuserver=None, username=None, password=None):
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

  def _authenticate(self):
    json_msg = ds_protocol.generate_authenticate_rq(self.username, self.password)
    self.sendfile.write(json_msg + '\r\n')
    self.sendfile.flush()

    response = self.recvfile.readline()
    parsed = ds_protocol.extract_json(response)

    if parsed.type == 'ok':
      self.token = parsed.token
    else:
      raise Exception(f"Authentication failed: {parsed.message}")

  def send(self, message:str, recipient:str) -> bool:
    # must return true if message successfully sent, false if send failed.
    try:
      timestamp = time.time()
      json_msg = ds_protocol.generate_directmessage_rq(self.token, message, recipient, timestamp)
      self.sendfile.write(json_msg + '\r\n')
      self.sendfile.flush()

      response = self.recvfile.readline()
      parsed = ds_protocol.extract_json(response)

      if parsed.type == "ok":
        return True
      else:
        return False

    except:
      return False

  def retrieve_new(self) -> list:
    # must return a list of DirectMessage objects containing all new messages
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
    # must return a list of DirectMessage objects containing all messages
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
  
  def close(self):
    """Cleanly close the connection."""
    self.sendfile.close()
    self.recvfile.close()
    self.client.close()