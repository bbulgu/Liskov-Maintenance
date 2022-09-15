
from pdfminer.psparser import PSBaseParser, PSKeywordTable, \
                              PSLiteralTable, PSStackParser, PSEOF
KWD = PSKeywordTable.intern
LIT = PSLiteralTable.intern


TESTDATA = br'''%!PS
begin end
 "  @ #
/a/BCD /Some_Name /foo#5f#xbaa
0 +1 -2 .5 1.234
(abc) () (abc ( def ) ghi)
(def\040\0\0404ghi) (bach\\slask) (foo\nbaa)
(this % is not a comment.)
(foo
baa)
(foo\
baa)
<> <20> < 40 4020 >
<abcd00
12345>
func/a/b{(c)do*}def
[ 1 (z) ! ]
<< /foo (bar) >>
'''

TOKENS = [
    (5, KWD(b'begin')), (11, KWD(b'end')), (16, KWD(b'"')), (19, KWD(b'@')),
    (21, KWD(b'#')), (23, LIT('a')), (25, LIT('BCD')), (30, LIT('Some_Name')),
    (41, LIT('foo_xbaa')), (54, 0), (56, 1), (59, -2), (62, 0.5),
    (65, 1.234), (71, b'abc'), (77, b''), (80, b'abc ( def ) ghi'),
    (98, b'def \x00 4ghi'), (118, b'bach\\slask'), (132, b'foo\nbaa'),
    (143, b'this % is not a comment.'), (170, b'foo\nbaa'), (180, b'foobaa'),
    (191, b''), (194, b' '), (199, b'@@ '), (211, b'\xab\xcd\x00\x124\x05'),
    (226, KWD(b'func')), (230, LIT('a')), (232, LIT('b')),
    (234, KWD(b'{')), (235, b'c'), (238, KWD(b'do*')), (241, KWD(b'}')),
    (242, KWD(b'def')), (246, KWD(b'[')), (248,
                                           1), (250, b'z'), (254, KWD(b'!')),
    (256, KWD(b']')), (258, KWD(b'<<')), (261, LIT('foo')), (266, b'bar'),
    (272, KWD(b'>>'))
]

OBJS = [
    (23, LIT('a')), (25, LIT('BCD')), (30, LIT('Some_Name')),
    (41, LIT('foo_xbaa')), (54, 0), (56, 1), (59, -2), (62, 0.5),
    (65, 1.234), (71, b'abc'), (77, b''), (80, b'abc ( def ) ghi'),
    (98, b'def \x00 4ghi'), (118, b'bach\\slask'), (132, b'foo\nbaa'),
    (143, b'this % is not a comment.'), (170, b'foo\nbaa'), (180, b'foobaa'),
    (191, b''), (194, b' '), (199, b'@@ '), (211, b'\xab\xcd\x00\x124\x05'),
    (230, LIT('a')), (232, LIT('b')), (234, [b'c']), (246, [1, b'z']),
    (258, {'foo': b'bar'}),
]


def get_tokens(s):
    from io import BytesIO

    class MyParser(PSBaseParser):
        def flush(self):
            self.add_results(*self.popall())

    parser = MyParser(BytesIO(s))
    r = []
    try:
        while True:
            r.append(parser.nexttoken())
    except PSEOF:
        pass
    return r


def get_objects(s):
    from io import BytesIO

    class MyParser(PSStackParser):
        def flush(self):
            self.add_results(*self.popall())
    parser = MyParser(BytesIO(s))
    r = []
    try:
        while True:
            r.append(parser.nextobject())
    except PSEOF:
        pass
    return r


def test_1():
    tokens = get_tokens(TESTDATA)
    print(tokens)
    print(TOKENS)
    assert all([a == b for a, b in zip(tokens, TOKENS)])


def test_2():
    objs = get_objects(TESTDATA)
    print(objs)
    assert (objs == OBJS)