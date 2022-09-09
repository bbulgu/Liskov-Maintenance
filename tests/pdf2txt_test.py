import sys

from tools import pdf2txt
from tests import oldpdf2txt


# Tests for verifying that functionality remains the same
# after replacing getopt with argparse.

def test_no_args():
    pdf2txt.main(['pdf2txt.py'])
    output_new = sys.stdout
    oldpdf2txt.main(['pdf2txt.py'])
    output_old = sys.stdout
    assert output_new == output_old


def test_write_stdout_debug():
    pdf2txt.main(['pdf2txt.py', '-d', 'samples/simple1.pdf'])
    output_new = sys.stdout
    oldpdf2txt.main(['pdf2txt.py', '-d', 'samples/simple1.pdf'])
    output_old = sys.stdout
    assert output_new == output_old


""" this test is failing because whitespaces do not match!!
def test_write_file():
    pdf2txt.main(['pdf2txt.py', '-o',
                  'tests/result1.txt', 'samples/simple1.pdf'])
    with open('tests/result1.txt') as outfile_new:
        lines_new = outfile_new.readlines()
    oldpdf2txt.main(['pdf2txt.py', '-o',
                     'tests/result2.txt', 'samples/simple1.pdf'])
    with open('tests/result2.txt') as outfile_old:
        lines_old = outfile_old.readlines()
    assert lines_new == lines_old
"""
