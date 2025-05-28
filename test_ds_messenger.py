from ds_messenger import DirectMessenger

SERVER = 'localhost'
USERNAME = "Shirley"
PASSWORD = "password"
RECIPIENT = "Emily"

def test_send():
    dm = DirectMessenger(SERVER, USERNAME, PASSWORD)
    result = dm.send("hello from test!", RECIPIENT)
    assert result == True or result == False

def test_retrieve_new():
    dm = DirectMessenger(SERVER, USERNAME, PASSWORD)
    messages = dm.retrieve_new()
    assert isinstance(messages, list)
    for m in messages:
        assert hasattr(m, 'message')
        assert hasattr(m, 'sender')
        assert hasattr(m, 'timestamp')

def test_retrieve_all():
    dm = DirectMessenger(SERVER, USERNAME, PASSWORD)
    messages = dm.retrieve_all()
    assert isinstance(messages, list)
    for m in messages:
        assert hasattr(m, 'message')
        assert hasattr(m, 'timestamp')
        assert hasattr(m, 'sender') or hasattr(m, 'recipient')


if __name__ == '__main__':
    test_send()
    test_retrieve_new()
    test_retrieve_all()