#!/usr/bin/env python
#
#  latin2ascii.py - converts latin1 characters into ascii.
#

import sys

""" Mappings from Latin-1 characters to ASCII.

This is an in-house mapping table for some Latin-1 characters
(acutes, umlauts, etc.) to ASCII strings.
"""

LATIN2ASCII = {
    # 0x00a0: '',
    # 0x00a7: '',
    # iso-8859-1
    0x00C0: "A`",
    0x00C1: "A'",
    0x00C2: "A^",
    0x00C3: "A~",
    0x00C4: "A:",
    0x00C5: "A%",
    0x00C6: "AE",
    0x00C7: "C,",
    0x00C8: "E`",
    0x00C9: "E'",
    0x00CA: "E^",
    0x00CB: "E:",
    0x00CC: "I`",
    0x00CD: "I'",
    0x00CE: "I^",
    0x00CF: "I:",
    0x00D0: "D'",
    0x00D1: "N~",
    0x00D2: "O`",
    0x00D3: "O'",
    0x00D4: "O^",
    0x00D5: "O~",
    0x00D6: "O:",
    0x00D8: "O/",
    0x00D9: "U`",
    0x00DA: "U'",
    0x00DB: "U~",
    0x00DC: "U:",
    0x00DD: "Y'",
    0x00DF: "ss",
    0x00E0: "a`",
    0x00E1: "a'",
    0x00E2: "a^",
    0x00E3: "a~",
    0x00E4: "a:",
    0x00E5: "a%",
    0x00E6: "ae",
    0x00E7: "c,",
    0x00E8: "e`",
    0x00E9: "e'",
    0x00EA: "e^",
    0x00EB: "e:",
    0x00EC: "i`",
    0x00ED: "i'",
    0x00EE: "i^",
    0x00EF: "i:",
    0x00F0: "d'",
    0x00F1: "n~",
    0x00F2: "o`",
    0x00F3: "o'",
    0x00F4: "o^",
    0x00F5: "o~",
    0x00F6: "o:",
    0x00F8: "o/",
    0x00F9: "o`",
    0x00FA: "u'",
    0x00FB: "u~",
    0x00FC: "u:",
    0x00FD: "y'",
    0x00FF: "y:",
    # Ligatures
    0x0152: "OE",
    0x0153: "oe",
    0x0132: "IJ",
    0x0133: "ij",
    0x1D6B: "ue",
    0xFB00: "ff",
    0xFB01: "fi",
    0xFB02: "fl",
    0xFB03: "ffi",
    0xFB04: "ffl",
    0xFB05: "ft",
    0xFB06: "st",
    # Symbols
    # 0x2013: '',
    0x2014: "--",
    0x2015: "||",
    0x2018: "`",
    0x2019: "'",
    0x201C: "``",
    0x201D: "''",
    # 0x2022: '',
    # 0x2212: '',
}


def latin2ascii(s):
    return "".join(LATIN2ASCII.get(ord(c), c) for c in s)


def main(argv):
    import getopt
    import fileinput

    def usage():
        print("usage: %s [-c codec] file ..." % argv[0])
        return 100

    try:
        (opts, args) = getopt.getopt(argv[1:], "c")
    except getopt.GetoptError:
        return usage()
    if not args:
        return usage()
    codec = "utf-8"
    for (k, v) in opts:
        if k == "-c":
            codec = v
    for line in fileinput.input(args):
        line = latin2ascii(unicode(line, codec, "ignore"))
        sys.stdout.write(line.encode("ascii", "replace"))
    return


if __name__ == "__main__":
    sys.exit(main(sys.argv))
