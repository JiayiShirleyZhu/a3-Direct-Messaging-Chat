# ICS 32
# Assignment #1: Diary
#
# Author: Aaron Imani
#
# v0.1.0

# You should review this code to identify what features you need to support
# in your program for assignment 1.
#
# YOU DO NOT NEED TO READ OR UNDERSTAND THE
# JSON SERIALIZATION ASPECTS OF THIS CODE
# RIGHT NOW, though can you certainly take a
# look at it if you are curious since we
# already covered a bit of the JSON format in class.

"""Defines the Notebook class for managing contacts and messages."""
from pathlib import Path
import json
import time
from ds_messenger import DirectMessage


class NotebookFileError(Exception):
    """
    NotebookFileError is a custom exception handler
    that you should catch in your own code. It
    is raised when attempting to load or save
    Notebook objects to file the system.
    """


class IncorrectNotebookError(Exception):
    """
    NotebookError is a custom exception handler
    that you should catch in your own code. It
    is raised when attempting to deserialize a
    notebook file to a Notebook object.
    """


class Diary(dict):
    """

    The Diary class is responsible for working with
    individual user diaries. It currently
    supports two features: A timestamp property that
    is set upon instantiation and
    when the entry object is set and an entry property
    that stores the diary message.

    """

    def __init__(self, entry: str = None, timestamp: float = 0) -> None:
        """
        Initializes a Diary entry.

        :param entry: The diary text content.
        :param timestamp: A timestamp for the diary, 0 if unset.
        """
        self._timestamp = timestamp
        self.set_entry(entry)
        dict.__init__(self, entry=self._entry, timestamp=self._timestamp)

    def set_entry(self, entry: str) -> None:
        """
        Sets the diary entry and updates timestamp if not yet set.

        :param entry: The diary text.
        """
        self._entry = entry
        dict.__setitem__(self, 'entry', entry)
        if self._timestamp == 0:
            self._timestamp = time.time()

    def get_entry(self) -> str:
        """Returns the diary entry."""
        return self._entry

    def set_time(self, timestamp: float) -> None:
        """Sets the timestamp."""
        self._timestamp = timestamp
        dict.__setitem__(self, 'timestamp', timestamp)

    def get_time(self) -> float:
        """Returns the timestamp."""
        return self._timestamp

    entry = property(get_entry, set_entry)
    timestamp = property(get_time, set_time)


class Notebook:
    """Notebook is a class that can be used to manage a diary notebook."""

    def __init__(self, username: str, password: str, bio: str = "") -> None:
        """Creates a new Notebook object.

        Args:
            username (str): The username of the user.
            password (str): The password of the user.
            bio (str): The bio of the user.
        """
        self.username = username
        self.password = password
        self.bio = bio
        self._diaries = []
        self._messages = []
        self._contacts = set()

    def add_diary(self, diary: Diary) -> None:
        """
        Adds a Diary object to the notebook.

        :param diary: A Diary instance to add.
        """
        self._diaries.append(diary)

    def del_diary(self, index: int) -> bool:
        """
        Deletes the diary at the specified index.

        :param index: Index of diary to delete.
        :return: True if successful, False if index was invalid.
        """
        try:
            del self._diaries[index]
            return True
        except IndexError:
            return False

    def get_diaries(self) -> list[Diary]:
        """
        Returns a list of all Diary objects in the notebook.

        :return: List of Diary entries.
        """
        return self._diaries

    def add_message(self, msg: DirectMessage) -> None:
        """
        Adds a DirectMessage to the notebook if it's not already stored.

        :param msg: The DirectMessage object to add.
        """
        for m in self._messages:
            if (m.sender == msg.sender and
                m.recipient == msg.recipient and
                m.timestamp == msg.timestamp and
                    m.message == msg.message):
                return
        self._messages.append(msg)
        if msg.sender:
            self._contacts.add(msg.sender)
        if msg.recipient:
            self._contacts.add(msg.recipient)

    def get_messages(self) -> list:
        """
        Returns all stored DirectMessages.

        :return: List of DirectMessage objects.
        """
        return self._messages

    def add_contact(self, contact: str) -> None:
        """
        Adds a contact to the notebook.

        :param contact: Username to add as contact.
        """
        self._contacts.add(contact)

    def get_contacts(self) -> list:
        """
        Returns all contact usernames.

        :return: List of contacts.
        """
        return list(self._contacts)

    def save(self, path: str) -> None:
        """
        Saves the notebook to the specified file path.

        :param path: JSON file path to save to.
        :raises NotebookFileError: If file write fails or path is invalid.
        """
        p = Path(path)
        p.touch(exist_ok=True)

        if p.suffix == '.json':
            try:
                with open(p, 'w', encoding='utf-8') as f:
                    json.dump({
                        "username": self.username,
                        "password": self.password,
                        "bio": self.bio,
                        "_diaries": [{"entry": d.entry,
                                      "timestamp": d.timestamp}
                                     for d in self._diaries],
                        "_messages": [msg.__dict__ for msg in self._messages],
                        "_contacts": list(self._contacts)
                    }, f, indent=4)
            except Exception as ex:
                raise NotebookFileError(
                    "Error while attempting to process the notebook file."
                ) from ex
        else:
            raise NotebookFileError("Invalid notebook file path or type")

    def load(self, path: str) -> None:
        """
        Loads notebook data from the specified file path.

        :param path: JSON file path to load from.
        :raises NotebookFileError: If the file does
        not exist or cannot be parsed.
        """
        p = Path(path)

        if not p.exists():
            with open(p, 'w', encoding='utf-8') as f:
                json.dump({
                    "username": self.username,
                    "password": self.password,
                    "bio": {"entry": "", "timestamp": ""},
                    "_diaries": [],
                    "_messages": [],
                    "_contacts": []
                }, f, indent=4)

        with open(p, 'r', encoding='utf-8') as f:
            obj = json.load(f)

        self.username = obj.get("username", "")
        self.password = obj.get("password", "")
        self.bio = obj.get("bio", {})
        self._diaries = [Diary(d['entry'], d['timestamp'])
                         for d in obj.get("_diaries", [])]
        self._contacts = set(obj.get("_contacts", []))

        self._messages = []
        for m in obj.get("_messages", []):
            dm = DirectMessage()
            dm.message = m["message"]
            dm.sender = m.get("sender", "")
            dm.recipient = m.get("recipient", "")
            dm.timestamp = m["timestamp"]
            self._messages.append(dm)
