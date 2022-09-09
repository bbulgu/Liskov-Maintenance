from pdfminer.arcfour import Arcfour


def test():
    assert Arcfour(b'Key').process(b'Plaintext').hex() \
           == 'bbf316e8d940af0ad3'
    assert Arcfour(b'Wiki').process(b'pedia').hex() \
           == '1021bf0420'
    assert Arcfour(b'Secret').process(b'Attack at dawn').hex() \
           == '45a01f645fc35b383552544b9bf5'
