from tools.pdf2txt import *
from pdfminer.layout import LAParams


def test_cmd():
    commandline(['pdf2txt.py', '-P', 'test', '../sample.pdf'])
    return


def test_pdfconversion():
    args = ['../sample.pdf']
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

    pdfconversion(args, password, pagenos, maxpages, outfile, outtype, imagewriter,
                  rotation, stripcontrol, layoutmode, encoding, scale,
                  caching, laparams, debug)
