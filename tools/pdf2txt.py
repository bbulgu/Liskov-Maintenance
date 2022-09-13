#!/usr/bin/env python
import argparse
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

# main


def main(argv):

    def usage():
        print(f'usage: {argv[0]} [-P password] [-o output]'
              ' [-t text|html|xml|tag]'
              ' [-O output_dir] [-c encoding] [-s scale] [-R rotation]'
              ' [-Y normal|loose|exact] [-p pagenos] [-m maxpages]'
              ' [-S] [-C] [-n] [-A] [-V] [-M char_margin] [-L line_margin]'
              ' [-W word_margin] [-F boxes_flow] [-d] input.pdf ...')
        return 100
    try:
        parser = argparse.ArgumentParser(description='Process arguments.')
        parser.add_argument('-P', help="password", type=str,
                            action='store', default='')
        parser.add_argument('-o', help="output", type=str, action='store')
        parser.add_argument('-t', help="text", type=str,
                            choices=['text', 'html', 'xml', 'tag'],
                            action='store', default='text')
        parser.add_argument('-O', help="output_dir", type=str, action='store')
        parser.add_argument('-c', help="encoding", type=str,
                            action='store', default='utf-8')
        parser.add_argument('-s', help="scale", type=float,
                            action='store', default=1)
        parser.add_argument('-R', help="rotation", type=int,
                            action='store', default=0)
        parser.add_argument('-Y', help="layoutmode", type=str,
                            choices=['normal', 'loose', 'exact'],
                            action='store', default='normal')
        parser.add_argument('-p', help="pagenos", type=int,
                            action='store', default=set())
        parser.add_argument('-m', help="maxpages", type=int,
                            action='store', default=0)
        parser.add_argument('-S', action='store_true', default=False)
        parser.add_argument('-C', action='store_true', default=True)
        parser.add_argument('-n', action='store_true', default=LAParams())
        parser.add_argument('-A', action='store_true', default=False)
        parser.add_argument('-V', action='store_true', default=False)
        parser.add_argument('-M', help='char_margin',
                            type=float, action='store')
        parser.add_argument('-L', help="line_margin",
                            type=float, action='store')
        parser.add_argument('-W', help="word_margin",
                            type=float, action='store')
        parser.add_argument('-F', help="boxes_flow",
                            type=float, action='store')
        parser.add_argument('-d', action='store_true')
        parser.add_argument('files', metavar='file',
                            help='the files you want to convert',
                            nargs=argparse.REMAINDER, default=[])
        args = parser.parse_args(argv[1:])
    except argparse.ArgumentError:
        return usage()
    if not args.files:
        return usage()
    # debug option
    debug = 1 if args.d else 0
    # input option
    password = args.p.encode('ascii') if args.p else b''
    pagenos = set()
    if args.p:
        pagenos.update(int(x) - 1 for x in args.p.split(','))
    maxpages = int(args.m) if args.m else 0
    # output option
    outfile = args.o if args.o else None
    outtype = args.t if args.t else None
    imagewriter = ImageWriter(args.O) if args.O else None
    rotation = int(args.R) if args.R else 0
    stripcontrol = args.S
    layoutmode = args.Y
    encoding = args.c
    scale = float(args.s)
    caching = not args.C
    laparams = None if args.n else LAParams()
    if laparams:
        laparams.all_texts = args.A
        laparams.detect_vertical = args.V
        laparams.char_margin = args.M
        laparams.word_margin = args.W
        laparams.line_margin = args.L
        laparams.boxes_flow = args.F

    #
    PDFDocument.debug = debug
    PDFParser.debug = debug
    CMapDB.debug = debug
    PDFPageInterpreter.debug = debug
    #
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
    elif outtype == 'html':
        device = HTMLConverter(rsrcmgr, outfp, scale=scale,
                               layoutmode=layoutmode, laparams=laparams,
                               imagewriter=imagewriter, debug=debug)
    elif outtype == 'tag':
        device = TagExtractor(rsrcmgr, outfp)
    else:
        return usage()

    for fname in args.files:
        with open(fname, 'rb') as fp:
            interpreter = PDFPageInterpreter(rsrcmgr, device)
            for page in PDFPage.get_pages(fp, pagenos,
                                          maxpages=maxpages, password=password,
                                          caching=caching,
                                          check_extractable=True):
                page.rotate = (page.rotate+rotation) % 360
                interpreter.process_page(page)
    device.close()
    if outfile:
        outfp.close()
    return


if __name__ == '__main__':
    sys.exit(main(sys.argv))
