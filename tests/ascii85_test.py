from pdfminer.ascii85 import ascii85decode, asciihexdecode


def test_decode():
    assert ascii85decode(b'9jqo^BlbD-BleB1DJ+*+F(f,q') == b'Man is distinguished'
    assert ascii85decode(b'E,9)oF*2M7/c~>') == b'pleasure.'


def test_hexdecode():
    assert asciihexdecode(b'61 62 2e6364   65') == b'ab.cde'
    assert asciihexdecode(b'61 62 2e6364   657>') == b'ab.cdep'
    assert asciihexdecode(b'7>') == b'p'