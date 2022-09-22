import os
from pdfminer.pdfdocument import PDFDocument, PDFNoOutlines
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
from tools import dumppdf


FNAME = "samples/sci.pdf"
INTRODUCTION = "tests/expected_introduction.txt"
REFERENCES = "tests/expected_references.txt"


def read_lines(filename):
    with open(filename, 'r', encoding='utf8') as fp:
        lines = fp.readlines()
    return lines


def test_generate_page_string():
    assert (dumppdf.generate_page_string(1, 3) == "2, 3, 4")
    assert (dumppdf.generate_page_string(4, 3) == "")


def test_get_start_end_pages_correct():
    with open(FNAME, 'rb') as fp:
        parser = PDFParser(fp)
        doc = PDFDocument(parser, b'')
        pages = dict((page.pageid, pageno) for (pageno, page)
                     in enumerate(PDFPage.create_pages(doc)))

        try:
            outlines = doc.get_outlines()
            start_page, end_page, end_title = dumppdf.get_start_end_pages(
                outlines, "Introduction", doc, pages)
            assert (start_page == 1)
            assert (end_page == 1)
            assert (end_title == "What is SCI-HUB?")
        except PDFNoOutlines:
            pass
        parser.close()


def test_get_start_end_pages_fails():
    with open(FNAME, 'rb') as fp:
        parser = PDFParser(fp)
        doc = PDFDocument(parser, b'')
        pages = dict((page.pageid, pageno) for (pageno, page)
                     in enumerate(PDFPage.create_pages(doc)))

        try:
            outlines = doc.get_outlines()
            start_page, end_page, end_title = dumppdf.get_start_end_pages(
                                                 outlines, "", doc, pages)
            assert (start_page is None)
            assert (end_page == 7)      # this pdf has 7 pages
            assert (end_title is None)
        except PDFNoOutlines:
            pass
        parser.close()


def test_get_start_end_pages_different():
    with open(FNAME, 'rb') as fp:
        parser = PDFParser(fp)
        doc = PDFDocument(parser, b'')
        pages = dict((page.pageid, pageno) for (pageno, page)
                     in enumerate(PDFPage.create_pages(doc)))

        try:
            outlines = doc.get_outlines()
            start_page, end_page, end_title = dumppdf.get_start_end_pages(
                outlines, "What is SCI-HUB?", doc, pages)
            assert (start_page == 1)
            assert (end_page == 3)      # this pdf has 7 pages
            assert (end_title == "Legal and Ethical Issues")
        except PDFNoOutlines:
            pass
        parser.close()


def test_write_to_outfile():
    dumppdf.write_to_outfile(
        '2', FNAME, "results/introduction.txt",
        "What is SCI-HUB?", "Introduction")
    lines = read_lines('results/introduction.txt')
    os.remove("results/introduction.txt")
    assert (lines == read_lines(INTRODUCTION))

# Testing the full implementation


def test_extract_Introduction():
    dumppdf.get_outlines_text(FNAME, "Introduction",
                              'results/introduction.txt', password=b'')
    lines = read_lines('results/introduction.txt')
    os.remove("results/introduction.txt")
    assert (lines == read_lines(INTRODUCTION))


def test_extract_References():
    dumppdf.get_outlines_text(
        FNAME, "References", 'results/references.txt', password=b'')
    lines = read_lines('results/references.txt')
    os.remove("results/references.txt")
    assert (lines == read_lines(REFERENCES))


def test_extract_wrong_outline():
    dumppdf.get_outlines_text("samples/sci.pdf", "What is SCI-HUBB?",
                              "results/whatis.txt")
    try:
        with open('results/whatis.txt', 'r', encoding='utf8'):
            assert False
    except FileNotFoundError:
        assert True
