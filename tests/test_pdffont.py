from pdfminer.pdffont import *


"""
Test get_widths with varying inputs 
"""
def test_get_widths():
    assert get_widths([1]) == {}
    assert get_widths([1, 2, 3]) == {1: 3, 2: 3}
    assert get_widths([1, [2, 3], 6, [7, 8]]) == {1: 2, 2: 3, 6: 7, 7: 8}


"""
Test get_widths2 with varying inputs 
"""
def test_get_widths2():
    assert get_widths2([1]) == {}
    assert get_widths2([1, 2, 3, 4, 5]) == {1: (3, (4, 5)), 2: (3, (4, 5))}
    assert get_widths2([1, [2, 3, 4, 5], 6, [7, 8, 9]]) == {1: (2, (3, 4)), 6: (7, (8, 9))}
