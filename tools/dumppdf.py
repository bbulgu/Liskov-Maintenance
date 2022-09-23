#!/usr/bin/env python
#
# dumppdf.py - dump pdf contents in XML format.
#
#  usage: dumppdf.py [options] [files ...]
#  options:
#    -i objid : object id
#
import sys
import os.path
from io import StringIO
from pdfminer.psparser import PSKeyword, PSLiteral, LIT
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument, PDFNoOutlines
from pdfminer.pdftypes import PDFObjectNotFound, PDFValueError
from pdfminer.pdftypes import PDFStream, PDFObjRef, resolve1, stream_value
from pdfminer.pdfpage import PDFPage
from pdfminer.utils import isnumber, q
from tools import pdf2txt


ESCAPE = set(map(ord, '&<>"'))


def encode(data):
    buf = StringIO()
    for b in data:
        if b < 32 or 127 <= b or b in ESCAPE:
            buf.write(f'&#{b};')
        else:
            buf.write(chr(b))
    return buf.getvalue()


# dumpxml
def dumpxml(out, obj, mode=None):
    if obj is None:
        out.write('<null />')
        return

    if isinstance(obj, dict):
        out.write('<dict size="%d">\n' % len(obj))
        for (k, v) in obj.items():
            out.write('<key>%s</key>\n' % k)
            out.write('<value>')
            dumpxml(out, v)
            out.write('</value>\n')
        out.write('</dict>')
        return

    if isinstance(obj, list):
        out.write('<list size="%d">\n' % len(obj))
        for v in obj:
            dumpxml(out, v)
            out.write('\n')
        out.write('</list>')
        return

    if isinstance(obj, bytes):
        out.write('<string size="%d">%s</string>' % (len(obj), encode(obj)))
        return

    if isinstance(obj, PDFStream):
        if mode == 'raw':
            out.buffer.write(obj.get_rawdata())
        elif mode == 'binary':
            out.buffer.write(obj.get_data())
        else:
            out.write('<stream>\n<props>\n')
            dumpxml(out, obj.attrs)
            out.write('\n</props>\n')
            if mode == 'text':
                data = obj.get_data()
                out.write(
                    '<data size="%d">%s</data>\n' %
                    (len(data), encode(data)))
            out.write('</stream>')
        return

    if isinstance(obj, PDFObjRef):
        out.write('<ref id="%d" />' % obj.objid)
        return

    if isinstance(obj, PSKeyword):
        out.write('<keyword>%s</keyword>' % obj.name)
        return

    if isinstance(obj, PSLiteral):
        out.write('<literal>%s</literal>' % obj.name)
        return

    if isnumber(obj):
        out.write('<number>%s</number>' % obj)
        return

    raise TypeError(obj)

# dumptrailers


def dumptrailers(out, doc):
    for xref in doc.xrefs:
        out.write('<trailer>\n')
        dumpxml(out, xref.trailer)
        out.write('\n</trailer>\n\n')
    return

# dumpallobjs


def dumpallobjs(out, doc, mode=None):
    visited = set()
    out.write('<pdf>')
    for xref in doc.xrefs:
        for objid in xref.get_objids():
            if objid in visited:
                continue
            visited.add(objid)
            try:
                obj = doc.getobj(objid)
                if obj is None:
                    continue
                out.write('<object id="%d">\n' % objid)
                dumpxml(out, obj, mode=mode)
                out.write('\n</object>\n\n')
            except PDFObjectNotFound as e:
                print(f'not found: {e!r}', file=sys.stderr)
    dumptrailers(out, doc)
    out.write('</pdf>')
    return


def resolve_dest(dest, doc):
    if isinstance(dest, str):
        dest = resolve1(doc.get_dest(dest))
    elif isinstance(dest, PSLiteral):
        dest = resolve1(doc.get_dest(dest.name))
    if isinstance(dest, dict):
        dest = dest['D']
    return dest


"""
Returns the page number for an outline,
given its destination (dest)
The required parameters of the function
(dest, a) are all part of the outline
doc contains the document as a whole
pages have all the information about the pages
"""


def get_page_number(dest, doc, pages, a):
    pageno = None
    if dest:
        dest = resolve_dest(dest, doc)
        pageno = pages[dest[0].objid]
    elif a:
        action = a.resolve()
        if isinstance(action, dict):
            subtype = action.get('S')
            if subtype and repr(
                    subtype) == '/GoTo' and action.get('D'):
                dest = resolve_dest(action['D'], doc)
                pageno = pages[dest[0].objid]
    return pageno


"""
Goes through all the outlines and extracts the
information, writing it to outfp (outputfile pointer).
doc contains the document as a whole
pages have all the information about the pages
dest_info is a boolean flag designating whether we
want to write the destination information to the file or not
outlines contain the outline information
"""


def extract_outline_info(pages, outlines, doc, outfp, dest_info):
    for (level, title, dest, a, se) in outlines:
        pageno = get_page_number(dest, doc, pages, a)
        s = q(title)
        outfp.write('<outline level="%r" title="%s">\n' %
                    (level, q(s)))
        if (dest_info):
            get_dest_info(dest, outfp)
        if pageno is not None:
            outfp.write('<pageno>%r</pageno>\n' % pageno)
        outfp.write('</outline>\n')


"""
Writes the destination to file if it is not None
dest: destination
outfp: outputfile pointer
"""


def get_dest_info(dest, outfp):
    if dest is not None:
        outfp.write('<dest>')
        dumpxml(outfp, dest)
        outfp.write('</dest>\n')


"""
A helper to generate a page string given start and end pages
A comma separated string of page numbers (required for pdf2txt)
Adds an offset of 1 since pdfminer starts on page 0
"""


def generate_page_string(start_page, end_page):
    st = ''
    for i in range(start_page+1, end_page+1):
        st += f'{i}, '
    if (start_page <= end_page):
        st += str(end_page+1)
    return st


"""
Given the outlines, doc, pages and the title/outline we're
looking for (target_title), return the page where we the
outline is (start_page), and where the next outline starts (end_page)
And the name of that outline (end_title)
"""


def get_start_end_pages(outlines, target_title, doc, pages):
    start_page = None
    end_page = None
    end_title = None
    for (x, title, dest, a, y) in outlines:
        # where to start reading
        if (title == target_title):
            start_page = get_page_number(dest, doc, pages, a)
        # we've already found the outline to start reading from
        elif start_page:
            # the next one is where we stop reading
            end_page = get_page_number(dest, doc, pages, a)
            end_title = title
            break

    if not end_page:    # if the outline we want to extract is the last one
        end_page = len(pages)

    return start_page, end_page, end_title


"""
Writes the given pages (st), from the file fname to a temporary file
Reads that file and writes only the text contained under our target_title
to end_title to outfile
"""


def write_to_outfile(st, fname, outfile, end_title, target_title):
    # write the text of the pdf document to a temporary file
    pdf2txt.main(['pdf2txt.py', '-o',
                  'tests/extracted.txt', '-p', st, fname])

    # read that file to extract the text between the two outlines
    with open('tests/extracted.txt', 'r', encoding='utf8') as fp:
        lines = fp.readlines()
        started_writing = False
        with open(outfile, 'w+', encoding='utf8') as outfp:
            for line in lines:
                # maybe a bug with PDFMiner, sometimes adds extra space
                line = line.replace("  ", " ")
                if end_title == line.rstrip():
                    break
                if target_title == line.rstrip():
                    started_writing = True
                if started_writing:
                    outfp.write(line)

    # remove the temporary file, since we don't need it anymore
    os.remove("tests/extracted.txt")


"""
Writes the text belonging to a particular outline specified by the
target_title, to a file called outname and reads the pdf from a file
called fname. Optionally takes in a password to open
an encrypted pdf.
"""


def get_outlines_text(fname, target_title, outfile, password=b''):
    with open(fname, 'rb') as fp:
        parser = PDFParser(fp)
        doc = PDFDocument(parser, password)
        pages = dict((page.pageid, pageno) for (pageno, page)
                     in enumerate(PDFPage.create_pages(doc)))

        try:
            outlines = doc.get_outlines()
            start_page, end_page, end_title = get_start_end_pages(
                outlines, target_title, doc, pages)

            # couldn't find the title, no text to get
            if not start_page:
                return

            st = generate_page_string(start_page, end_page)

            write_to_outfile(st, fname, outfile, end_title, target_title)

        except PDFNoOutlines:
            pass
        parser.close()
    return


def dumpoutline(outfp, fname, objids, pagenos, password=b'',
                dumpall=False, mode=None, extractdir=None, dest_info=True):
    with open(fname, 'rb') as fp:
        parser = PDFParser(fp)
        doc = PDFDocument(parser, password)
        pages = dict((page.pageid, pageno) for (pageno, page)
                     in enumerate(PDFPage.create_pages(doc)))

        try:
            outlines = doc.get_outlines()
            outfp.write('<outlines>\n')
            extract_outline_info(pages, outlines, doc, outfp, dest_info)
            outfp.write('</outlines>\n')
        except PDFNoOutlines:
            pass
        parser.close()
    return


# extractembedded
LITERAL_FILESPEC = LIT('Filespec')
LITERAL_EMBEDDEDFILE = LIT('EmbeddedFile')


def extractembedded(outfp, fname, objids, pagenos, password=b'',
                    dumpall=False, mode=None, extractdir=None):
    def extract1(obj):
        filename = os.path.basename(obj['UF'] or obj['F'])
        fileref = obj['EF']['F']
        fileobj = doc.getobj(fileref.objid)
        if not isinstance(fileobj, PDFStream):
            raise PDFValueError(
                'unable to process PDF: reference for %r is not a PDFStream' %
                (filename))
        if fileobj.get('Type') is not LITERAL_EMBEDDEDFILE:
            raise PDFValueError(
                'unable to process PDF: reference for %r is not an '
                'EmbeddedFile' %
                (filename))
        path = os.path.join(extractdir, filename)
        if os.path.exists(path):
            raise IOError('file exists: %r' % path)
        print(f'extracting: {path!r}', file=sys.stderr)
        with open(path, 'wb') as out:
            out.write(fileobj.get_data())
        return

    with open(fname, 'rb') as fp:
        parser = PDFParser(fp)
        doc = PDFDocument(parser, password)
        for xref in doc.xrefs:
            for objid in xref.get_objids():
                obj = doc.getobj(objid)
                if isinstance(obj, dict) and obj.get(
                        'Type') is LITERAL_FILESPEC:
                    extract1(obj)
    return

# dumppdf


def dumppdf(outfp, fname, objids, pagenos, password=b'',
            dumpall=False, mode=None, extractdir=None):
    with open(fname, 'rb') as fp:
        parser = PDFParser(fp)
        doc = PDFDocument(parser, password)
        if objids:
            for objid in objids:
                obj = doc.getobj(objid)
                dumpxml(outfp, obj, mode=mode)
        if pagenos:
            for (pageno, page) in enumerate(PDFPage.create_pages(doc)):
                if pageno in pagenos:
                    if mode is not None:
                        for obj in page.contents:
                            obj = stream_value(obj)
                            dumpxml(outfp, obj, mode=mode)
                    else:
                        dumpxml(outfp, page.attrs)
        if dumpall:
            dumpallobjs(outfp, doc, mode=mode)
        if (not objids) and (not pagenos) and (not dumpall):
            dumptrailers(outfp, doc)
        if mode not in ('raw', 'binary'):
            outfp.write('\n')
    return


# main
def main(argv):
    import getopt

    def usage():
        print(
            f'usage: {argv[0]} [-P password] [-a] [-p pageid] [-i objid] '
            '[-o output] [-r|-b|-t] [-T] [-O output_dir] [-d] input.pdf ...')
        return 100
    try:
        (opts, args) = getopt.getopt(argv[1:], 'dP:ap:i:o:rbtTO:')
    except getopt.GetoptError:
        return usage()
    if not args:
        return usage()
    debug = 0
    objids = []
    pagenos = set()
    mode = None
    password = b''
    dumpall = False
    proc = dumppdf
    outfp = sys.stdout
    extractdir = None
    for (k, v) in opts:
        if k == '-d':
            debug += 1
        elif k == '-P':
            password = v.encode('ascii')
        elif k == '-a':
            dumpall = True
        elif k == '-p':
            pagenos.update(int(x) - 1 for x in v.split(','))
        elif k == '-i':
            objids.extend(int(x) for x in v.split(','))
        elif k == '-o':
            outfp = open(v, 'wb')
        elif k == '-r':
            mode = 'raw'
        elif k == '-b':
            mode = 'binary'
        elif k == '-t':
            mode = 'text'
        elif k == '-T':
            proc = dumpoutline
        elif k == '-O':
            extractdir = v
            proc = extractembedded
    #
    PDFDocument.debug = debug
    PDFParser.debug = debug
    #
    for fname in args:
        proc(outfp, fname, objids, pagenos, password=password,
             dumpall=dumpall, mode=mode, extractdir=extractdir)
    return


if __name__ == '__main__':
    sys.exit(main(sys.argv))
