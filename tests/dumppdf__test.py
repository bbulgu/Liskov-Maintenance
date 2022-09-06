from tools.dumppdf import dumpoutline
import os

OUTLINES = ['<outlines>\n', '<outline level="1" title="Introduction">\n',
            '</outline>\n',
            '<outline level="1" title="Background">\n',
            '</outline>\n',
            '<outline level="2" title="Virtual Meeting Room">\n',
            '</outline>\n',
            '<outline level="2" title="Escape Room">\n',
            '</outline>\n',
            '<outline level="2" title="Active Learning in Escape Rooms">\n',
            '</outline>\n',
            '<outline level="2" title="External Stakeholder">\n',
            '</outline>\n', '</outlines>\n']


def test_dumpoutline():

    output_results = open('tests/outlines.txt', 'w+')
    dumpoutline(output_results, 'samples/outline.pdf', None, None)
    output_results.close()
    with open('tests/outlines.txt', 'r') as f:
        results = f.readlines()
        f.close()
        os.remove('tests/outlines.txt')
        print(results)
        assert (results == OUTLINES)
