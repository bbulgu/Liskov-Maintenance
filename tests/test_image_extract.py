import os

from tools.pdf2txt import *  # Importing all for now, TODO: change later for unambigous imports
import sys

PNG = 'samples/PNG.pdf'
JPG = 'samples/JPG.pdf'

DIR = 'tests/output-pictures'


def assert_file(extension):
    found_file = False

    for file in os.listdir(DIR):
        if file.endswith(extension):
            found_file = True
            os.remove(os.path.join(DIR, file))

    assert found_file


def test_jpg():
    assert commandline(
        ['pdf2text.py', '-o', 'tests/test_jpg', '-t', 'text', '-O', DIR,
         JPG]) == 0
    assert_file('.jpg')


# Creates a file called something starting with X that should be a png-file
def test_png():
    assert commandline(
        ['pdf2text.py', '-X', '-o', 'tests/test_png', '-t', 'text', '-O', DIR,
         PNG]) == 0
    assert_file('.png')
