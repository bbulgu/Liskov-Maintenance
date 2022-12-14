#!/usr/bin/env python
import sys
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfdevice import TagExtractor
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import XMLConverter, HTMLConverter, TextConverter
from pdfminer.cmapdb import CMapDB
from pdfminer.layout import LAParams
from pdfminer.image import ImageWriter

"""
Prints how the tool should be used.
"""


def usage():
    print('usage: pdf2txt.py [-P password] [-o output] [-O output_dir]'
          ' [-t text|html|xml|tag|xml-c|xml-w|xml-l] [-c encoding] [-s scale]'
          ' [-R rotation] [-Y normal|loose|exact] [-p pagenos] [-m maxpages]'
          ' [-S] [-C] [-n] [-A] [-V] [-M char_margin] [-L line_margin]'
          ' [-W word_margin] [-F boxes_flow] [-d] input.pdf ...')
    return 100


"""
Extracts the commandline arguments and declares them to independant variables
and calls pdfconversion with the corresponding arguments
"""


def commandline(argv):
    import getopt

    try:
        (opts, args) = getopt.getopt(
            argv[1:], 'dP:o:t:O:c:s:R:Y:p:m:SXCnAVM:W:L:F:')
    except getopt.GetoptError:
        return usage()
    if not args:
        return usage()

    # debug option
    debug = 0
    # input option
    password = b''
    pagenos = set()
    maxpages = 0
    # output option
    outfile = None
    outtype = None
    imagewriter = None
    rotation = 0
    stripcontrol = False
    layoutmode = 'normal'
    encoding = 'utf-8'
    scale = 1
    caching = True
    laparams = LAParams()
    png = False

    for (k, v) in opts:
        if k == '-d':
            debug += 1
        elif k == '-P':
            password = v.encode('ascii')
        elif k == '-o':
            outfile = v
        elif k == '-t':
            outtype = v
        elif k == '-X':
            png = True
        elif k == '-O':
            imagewriter = ImageWriter(v)
        elif k == '-c':
            encoding = v
        elif k == '-s':
            scale = float(v)
        elif k == '-R':
            rotation = int(v)
        elif k == '-Y':
            layoutmode = v
        elif k == '-p':
            pagenos.update(int(x) - 1 for x in v.split(','))
        elif k == '-m':
            maxpages = int(v)
        elif k == '-S':
            stripcontrol = True
        elif k == '-C':
            caching = False
        elif k == '-n':
            laparams = None
        elif k == '-A':
            laparams.all_texts = True
        elif k == '-V':
            laparams.detect_vertical = True
        elif k == '-M':
            laparams.char_margin = float(v)
        elif k == '-W':
            laparams.word_margin = float(v)
        elif k == '-L':
            laparams.line_margin = float(v)
        elif k == '-F':
            laparams.boxes_flow = float(v)
    #
    if png:
        imagewriter.set_png(True)

    PDFDocument.debug = debug
    PDFParser.debug = debug
    CMapDB.debug = debug
    PDFPageInterpreter.debug = debug
    #
    return pdfconversion(
        args,
        password,
        pagenos,
        maxpages,
        outfile,
        outtype,
        imagewriter,
        rotation,
        stripcontrol,
        layoutmode,
        encoding,
        scale,
        caching,
        laparams,
        debug)


"""
Converts pdf to specified output format and filetype.
"""


def pdfconversion(
        args,
        password,
        pagenos,
        maxpages,
        outfile,
        outtype,
        imagewriter,
        rotation,
        stripcontrol,
        layoutmode,
        encoding,
        scale,
        caching,
        laparams,
        debug):
    rsrcmgr = PDFResourceManager(caching=caching)
    if not outtype:
        outtype = 'text'
        if outfile:
            if outfile.endswith('.htm') or outfile.endswith('.html'):
                outtype = 'html'
            elif outfile.endswith('.xml'):
                outtype = 'xml'
            elif outfile.endswith('.tag'):
                outtype = 'tag'
    if outfile:
        outfp = open(outfile, 'w', encoding=encoding)
    else:
        outfp = sys.stdout
    if outtype == 'text':
        device = TextConverter(rsrcmgr, outfp, laparams=laparams,
                               imagewriter=imagewriter)
    elif outtype == 'xml':
        device = XMLConverter(rsrcmgr, outfp, laparams=laparams,
                              imagewriter=imagewriter,
                              stripcontrol=stripcontrol)
    elif 'xml' in outtype:
        coor_type = outtype[-1]
        device = XMLConverter(rsrcmgr, outfp, laparams=laparams,
                              imagewriter=imagewriter,
                              stripcontrol=stripcontrol,
                              coordinates_type=coor_type)
    elif outtype == 'html':
        device = HTMLConverter(rsrcmgr, outfp, scale=scale,
                               layoutmode=layoutmode, laparams=laparams,
                               imagewriter=imagewriter, debug=debug)
    elif outtype == 'tag':
        device = TagExtractor(rsrcmgr, outfp)
    else:
        return usage()
    for fname in args:
        with open(fname, 'rb') as fp:
            interpreter = PDFPageInterpreter(rsrcmgr, device)
            for page in PDFPage.get_pages(
                    fp,
                    pagenos,
                    maxpages=maxpages,
                    password=password,
                    caching=caching,
                    check_extractable=True):
                page.rotate = (page.rotate + rotation) % 360
                interpreter.process_page(page)
    device.close()

    if outfp != sys.stdout:
        outfp.close()

    return 0


# main
def main(argv):
    return commandline(argv)


if __name__ == '__main__':
    sys.exit(main(sys.argv))
