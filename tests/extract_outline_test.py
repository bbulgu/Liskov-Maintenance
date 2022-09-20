import os
from pdfminer.pdfdocument import PDFDocument, PDFNoOutlines
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
from tools import pdf2txt
from tools import dumppdf

introduction = """Introduction 
Prices for academic journals, particularly science journals, have been on the rise 
for decades.1 For researchers without access to an institutional library, these 
cost increases have come to mean paying $30 or more for each journal article 
they need to read. When they need to read hundreds of papers, these costs 
quickly become unmanageable. In 2011, a researcher in Kazakhstan created a 
website call Sci-Hub that allows anyone to access the full text of millions of 
scientific articles for free. Librarians should be aware of Sci-Hub because many 
of their patrons are already using it, and it will undoubtedly affect their expec-
tations about what their library should provide and how quickly they should be 
able to get articles. Librarians should also understand the risks that Sci-Hub can 
pose to their patrons, their institutions, and themselves. 

"""

references = """References 

1. Rose-Wiles, Lisa M. “The High Cost of Science Journals: A Case Study and Discussion.” 
Journal of Electronic Resources Librarianship 23 no. 3 (September 20, 2011): 219–241. 
doi:10.1080/1941126X.2011.601225. 

2. “Sci-Hub: Removing Barriers in the Way of Science.” Accessed September 6, 2016. http:// 

sci-hub.bz/. 

3. “Elsevier Inc. et al. v. Sci-Hub et al. “Docket Item 50 | United States Courts Archive.” 
September 15, 2015. https://www.unitedstatescourts.org/federal/nysd/442951/50-0.html. 
4. Bohannon, John. “Who’s Downloading Pirated Papers? Everyone.” Science 352, no. 6285 

(April 29, 2016): 508–512. doi:10.1126/science.352.6285.508. 

5. Bohannon, John. “The Frustrated Science Student behind Sci-Hub.” Science 352, no. 6285 

(April 29, 2016): 511. doi:10.1126/science.352.6285.511. 

6. Cabanac, Guillaume. “Bibliogifts in LibGen? A Study of a Text-Sharing Platform Driven 
by Biblioleaks and Crowdsourcing.” Journal of the Association for Information Science and 
Technology 67, no. 4 (March 27, 2015): 874–884. doi:10.1002/asi.23445. 

7. “Does Sci-Hub Phish for Credentials?” Sauropod Vertebra Picture of the Week. February 

25, 2016. https://svpow.com/2016/02/25/does-sci-hub-phish-for-credentials/. 

8. Banks, Marcus. “Sci-Hub: What It Is and Why It Matters.” American Libraries Magazine, 
May 31, 2016. https://americanlibrariesmagazine.org/2016/05/31/why-sci-hub-matters/. 
9. Smith, David. “Sci-Hub: How Does It Work?” The Scholarly Kitchen. February 25, 2016. 

https:/scholarlykitchen.sspnet.org/2016/02/25/sci-hub-how-does-it-work/. 

10. Waddell, Kaveh. “The Research Pirates of the Dark Web.” The Atlantic, February 9, 2016. 
http://www.theatlantic.com/technology/archive/2016/02/the-research-pirates-of-the-dark- 
web/461829/. 

11. Association of American Publishers. “AAP Statement on Sci-Hub.” May 10, 2016. http:// 

newsroom.publishers.org/aap-statement-on-sci-hub. 

12. Library of Congress, Copyright Office. “International Copyright Relations of the United 

States.”  Accessed October 20, 2016. http://purl.access.gpo.gov/GPO/LPS101162. 

13. Bendezú-Quispe, Guido, Wendy Nieto-Gutiérrez, Josmel Pacheco-Mendoza, and Alvaro 
Taype-Rondan. “Sci-Hub and Medical Practice: An Ethical Dilemma in Peru.” The Lancet 
Global Health 4, no. 9 (September, 2016): e608. doi:10.1016/S2214-109X(16)30188-7. 

14. Dobbs, David. “Testify: The Open-Science Movement Catches Fire.” WIRED. January 30, 

2012. https://www.wired.com/2012/01/testify-the-open-science-movement-catches-fire/. 

15. McNutt, Marcia. “My Love-Hate of Sci-Hub.” Science 352, no. 6285 (April 29, 2016): 497. 

doi:10.1126/science.aaf9419. 

16. Zipf, George Kingsley. Human Behavior and the Principle of Least Effort: An Introduction 

to Human Ecology. Cambridge, MA: Addison-Wesley Press, 1949. 

17. Ruff, Corinne. “Librarians Find Themselves Caught Between Journal Pirates and 
Publishers.” February 18, 2016. The Chronicle of Higher Education. http://www.chronicle. 
com/article/Librarians-Find-Themselves/235353/. 

View publication stats
View publication stats

"""

fname = "samples/sci.pdf"

# testing the helper functions


def test_generate_page_string():
    assert (dumppdf.generate_page_string(1, 3) == "2, 3, 4")
    assert (dumppdf.generate_page_string(4, 3) == "")


def test_get_start_end_pages_correct():
    with open(fname, 'rb') as fp:
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
    with open(fname, 'rb') as fp:
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
    with open(fname, 'rb') as fp:
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
        '2', fname, "results/introduction.txt",
        "What is SCI-HUB?", "Introduction")
    with open('results/introduction.txt', 'r', encoding='utf8') as fp:
        lines = fp.readlines()
    os.remove("results/introduction.txt")
    assert ("".join(lines) == introduction)

# Testing the full implementation


def test_extract_Introduction():
    dumppdf.get_outlines_text(fname, "Introduction",
                              'results/introduction.txt', password=b'')
    with open('results/introduction.txt', 'r', encoding='utf8') as fp:
        lines = fp.readlines()
    os.remove("results/introduction.txt")
    assert ("".join(lines) == introduction)


def test_extract_References():
    dumppdf.get_outlines_text(
        fname, "References", 'results/references.txt', password=b'')
    with open('results/references.txt', 'r', encoding='utf8') as fp:
        lines = fp.readlines()
    os.remove("results/references.txt")
    assert ("".join(lines) == references)


def test_extract_wrong_outline():
    dumppdf.get_outlines_text("samples/sci.pdf", "What is SCI-HUBB?",
                              "results/whatis.txt")
    try:
        with open('results/whatis.txt', 'r', encoding='utf8'):
            assert False
    except FileNotFoundError:
        assert True
