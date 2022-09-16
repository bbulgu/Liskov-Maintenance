from tools.pdf2txt import commandline, pdfconversion
from pdfminer.layout import LAParams

"""
Tests the commandline part of pdf2txt.py
"""


def usage():
    return 100


def test_cmd():
    assert commandline(['pdf2txt.py', '-P', 'test', './sample.pdf']) == 0


"""
Tests the pdf conversion part of pdf2txt.py
"""


def test_pdfconversion():
    args = ['./sample.pdf']
    password = b'test'
    pagenos = set()
    maxpages = 0
    outfile = None
    outtype = None
    imagewriter = None
    rotation = 0
    stripcontrol = False
    layoutmode = 'normal'
    encoding = 'utf-8'
    scale = 1
    caching = True
    debug = False
    laparams = LAParams()
    laparams.char_margin = 2.0
    laparams.line_margin = 0.5
    laparams.word_margin = 0.1
    laparams.all_texts = False

    assert pdfconversion(args, password, pagenos, maxpages, outfile, outtype,
                         imagewriter, rotation, stripcontrol, layoutmode,
                         encoding, scale, caching, laparams, debug) == 0


def test_xml_word_empty():
    assert commandline(['pdf2txt.py', '-t', 'xml']) == 100


def test_xml_char_no_specification(capfd):
    commandline(['pdf2txt.py', '-t', 'xml', 'samples/line.pdf'])
    out, err = capfd.readouterr()

    with open('samples/xml_output_line_char.txt', 'r') as file:
        data = file.read()

    assert out == data


def test_xml_char(capfd):
    commandline(['pdf2txt.py', '-t', 'xml|c', 'samples/line.pdf'])
    out, err = capfd.readouterr()

    with open('samples/xml_output_line_char.txt', 'r') as file:
        data = file.read()

    assert out == data


def test_xml_word(capfd):
    commandline(['pdf2txt.py', '-t', 'xml|w', 'samples/line.pdf'])
    out, err = capfd.readouterr()

    with open('samples/xml_output_line_word.txt', 'r') as file:
        data = file.read()

    assert out == data


def test_xml_line(capfd):
    commandline(['pdf2txt.py', '-t', 'xml|l', 'samples/line.pdf'])
    out, err = capfd.readouterr()

    with open('samples/xml_output_line_line.txt', 'r') as file:
        data = file.read()

    assert out == data
