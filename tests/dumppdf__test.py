from tools.dumppdf import *

def test_outline():
    with open('test.txt', 'a') as outputfile:
        dumpoutline(outputfile, './samples/simple1.pdf', None, None)
