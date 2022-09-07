import sys
import filecmp

from tools import pdf2txt
from tests import oldpdf2txt

def test():
    # Tests for verifying that functionality remains the same after replacing getopt with argparse.
    # No arguments
    pdf2txt.main(['pdf2txt.py'])
    output_new = sys.stdout
    oldpdf2txt.main(['pdf2txt.py'])
    output_old = sys.stdout
    assert output_new == output_old

    # Using default values
    pdf2txt.main(['pdf2txt.py', '-o', '../tests/result1.txt', '../samples/simple1.pdf'])
    with open('../tests/result1.txt') as outfile_new:
        lines_new = outfile_new.readlines()
    oldpdf2txt.main(['pdf2txt.py', '-o', '../tests/result2.txt', '../samples/simple1.pdf'])
    with open('../tests/result2.txt') as outfile_old:
        lines_old = outfile_old.readlines()
    assert lines_new == lines_old
    # Clearing files to make sure old results don't affect future tests.
    #open('../tests/result1.txt', 'w+')
    #open('../tests/result2.txt', 'w+')

    # Altering default values (in this case -t html)
    pdf2txt.main(['pdf2txt.py', '-o', '../tests/result1.html', '-t', 'html', '../samples/simple1.pdf'])
    with open('../tests/result1.html') as outfile_new:
        lines_new = outfile_new.readlines()
    oldpdf2txt.main(['pdf2txt.py', '-o', '../tests/result2.html', '-t', 'html', '../samples/simple1.pdf'])
    with open('../tests/result2.html') as outfile_old:
        lines_old = outfile_old.readlines()
    assert lines_new == lines_old
    # Clearing files to make sure old results don't affect future tests.
    #open('../tests/result1.html', 'w+')
    #open('../tests/result2.html', 'w+')

test()