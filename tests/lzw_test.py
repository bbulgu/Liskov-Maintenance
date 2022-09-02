from pdfminer.lzw import lzwdecode


def test_decode():
    assert lzwdecode(bytes.fromhex('800b6050220c0c8501')) == b'-----A---B'