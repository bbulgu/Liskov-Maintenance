from tools.pdf2txt import * # Importing all for now, TODO: change later for unambigous imports
import sys

PNG = 'samples/PNG.pdf'
JPG = 'samples/JPG.pdf'

#def test_jpg():
#    commandline(['pdf2text.py','-o', 'tests/test_jpg', '-t', 'text', '-O', 'tests/', JPG])
#    return


# Creates a file called something starting with X that should be a png-file
def test_jpg():
    commandline(['pdf2text.py','-o', 'tests/test_png', '-t', 'text', '-O', 'tests/', PNG])
    return