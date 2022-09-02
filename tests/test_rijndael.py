from pdfminer.rijndael import *

"""
Test encryption of data using key.
"""


def test_encryptor():
    key = bytes.fromhex('00010203050607080a0b0c0d0f101112')
    plaintext = bytes.fromhex('506812a45f08c889b97f5980038b8359')
    assert RijndaelEncryptor(key, 128).encrypt(plaintext).hex() == 'd8f532538289ef7d06b506a4fd5be9c9'


"""
Test decryption of data using key.
"""


def test_decryptor():
    key = bytes.fromhex('00010203050607080a0b0c0d0f101112')
    ciphertext = bytes.fromhex('d8f532538289ef7d06b506a4fd5be9c9')
    assert RijndaelDecryptor(key, 128).decrypt(ciphertext).hex() == '506812a45f08c889b97f5980038b8359'
