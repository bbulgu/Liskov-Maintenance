from pdfminer.runlength import rldecode

"""
Tests runlength decode with data provided by the former maintainer of
the repo.
"""


def test_rldecode():
    s = b'\x05123456\xfa7\x04abcde\x80junk'
    assert rldecode(s) == b'1234567777777abcde'
