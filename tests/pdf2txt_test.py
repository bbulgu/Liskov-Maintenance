import sys
import filecmp

from tools import pdf2txt
from tests import oldpdf2txt

def test_no_args():
    # Tests for verifying that functionality remains the same after replacing getopt with argparse.
    # No arguments
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


