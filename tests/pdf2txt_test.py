import sys
import filecmp

from tools import pdf2txt
from tests import oldpdf2txt

def test():
    pdf2txt.main(["pdf2txt.py"])
    output_new = sys.stdout
    oldpdf2txt.main(["pdf2txt.py"])
    output_old = sys.stdout
    assert output_new == output_old

    pdf2txt.main(["pdf2txt.py", "-o", "../tests/simple1.html", "-t", "html", "../samples/simple1.pdf"])
    with open("../tests/simple1.html") as outfile_new:
        lines_new = outfile_new.readlines()
    oldpdf2txt.main(["pdf2txt.py", "-o", "../tests/simple1.html", "-t", "html", "../samples/simple1.pdf"])
    with open("../tests/simple1.html") as outfile_old:
        lines_old = outfile_old.readlines()
    assert lines_new == lines_old

    pdf2txt.main(["pdf2txt.py", "samples/simple1.pdf"])
    with open("samples/simple1.txt") as outfile_new:
        lines_new = outfile_new.readlines()
    oldpdf2txt.main(["pdf2txt.py", "samples/simple1.pdf"])
    with open("samples/simple1.txt") as outfile_old:
        lines_old = outfile_old.readlines()
    assert lines_new == lines_old

test()