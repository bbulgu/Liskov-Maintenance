from pdfminer.psparser import PSBaseParser, KWD


def assert_parse_main(bytes, expected_parse1, exected_curtoken):
    fp = open('samples/sci.pdf', 'r')
    psb = PSBaseParser(fp=fp)

    assert psb._parse_main(bytes, 0) == 1

    if expected_parse1 is not None:
        assert psb._parse1 == expected_parse1(psb)

    if exected_curtoken is not None:
        assert psb._curtoken == exected_curtoken

    fp.close()
    return psb


def test__parse_main_percent():
    assert_parse_main(b'%', lambda psb: psb._parse_comment, b'%')


def test__parse_main_slash():
    assert_parse_main(b'/', lambda psb: psb._parse_literal, b'')


def test__parse_main_plus():
    assert_parse_main(b'+', lambda psb: psb._parse_number, b'+')


def test__parse_main_dot():
    assert_parse_main(b'.', lambda psb: psb._parse_float, b'.')


def test__parse_main_a():
    assert_parse_main(b'a', lambda psb: psb._parse_keyword, b'a')


def test__parse_main_parentheses():
    assert_parse_main(b'(', lambda psb: psb._parse_string, b'')


def test__parse_main_wopen():
    assert_parse_main(b'<', lambda psb: psb._parse_wopen, b'')


def test__parse_main_wclose():
    assert_parse_main(b'>', lambda psb: psb._parse_wclose, b'')


def test__parse_main_new_token():
    psb = assert_parse_main(b'*', None, None)
    assert psb._tokens == [(0, KWD(b'*'))]
