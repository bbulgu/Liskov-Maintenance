from tools import pdf2txt
from tools import dumppdf

introduction = """Prices for academic journals, particularly science journals, have been on the rise
for decades.1 For researchers without access to an institutional library, these
cost increases have come to mean paying $30 or more for each journal article
they need to read. When they need to read hundreds of papers, these costs
quickly become unmanageable. In 2011, a researcher in Kazakhstan created a
website call Sci-Hub that allows anyone to access the full text of millions of
scientific articles for free. Librarians should be aware of Sci-Hub because many
of their patrons are already using it, and it will undoubtedly affect their expec-
tations about what their library should provide and how quickly they should be
able to get articles. Librarians should also understand the risks that Sci-Hub can
pose to their patrons, their institutions, and themselves."""

def test_extract_outline():

    pdf2txt.main(['pdf2txt.py', '-o', 
                  'tests/extracted.txt', '-p', '2', 'samples/sci.pdf'])
    
    with open('tests/extracted.txt', 'r', encoding='utf8') as fp:
        lines = fp.readlines()
        for line in lines:
            print(line)


    """
    dumppdf.main(['dumppdf.py', '-t', 'samples/sci.pdf'])
    
    with open('tests/results/sci.txt') as outfile_new:
        lines_new = outfile_new.readlines()
    assert lines_new == lines_old
    """
    #assert ( == introduction)