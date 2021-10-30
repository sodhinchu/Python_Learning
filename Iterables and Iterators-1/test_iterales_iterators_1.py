import pytest
import sys
import inspect
import os
import re

import polygon
from polygon import Polygon
import polygonseqtype
from polygonseqtype import PolygonSeqType

README_CONTENT_CHECK_FOR = [
    "Iterable",
    "Iterator",
    "iter",
    "next",
    "getitem",
    "iteration",
    "indexing",
    "for",
    "while",
    "StopIteration",
    "exhausts",
    "custom"
]

def test_readme_exists():
    assert os.path.isfile("README.md"), "README.md file missing!"

def test_readme_contents():
    readme = open("README.md", "r")
    readme_words = readme.read().split()
    readme.close()
    assert len(readme_words) >= 500, "Make your README.md file interesting! Add atleast 500 words"

def test_readme_proper_description():
    READMELOOKSGOOD = True
    f = open("README.md", "r", encoding="utf-8")
    content = f.read()
    f.close()
    for c in README_CONTENT_CHECK_FOR:
        if c not in content:
            READMELOOKSGOOD = False
            pass
    assert READMELOOKSGOOD == True, "You have not described all the functions/class well in your README.md file"

def test_readme_file_for_formatting():
    f = open("README.md", "r", encoding="utf-8")
    content = f.read()
    f.close()
    assert content.count("#") >= 10

def test_indentations():
    ''' Returns pass if used four spaces for each level of syntactically \
    significant indenting.'''
    sources = [polygon, polygonseqtype]
    for source in sources:
        lines = inspect.getsource(polygon)
        spaces = re.findall('\n +.', lines)
        for space in spaces:
            assert len(space) % 4 == 2, "Your script contains misplaced indentations"
            assert len(re.sub(r'[^ ]', '', space)) % 4 == 0, "Your code indentation does not follow PEP8 guidelines"

def test_function_name_had_cap_letter():
    sources = [polygon, polygonseqtype]
    for source in sources:
        functions = inspect.getmembers(source, inspect.isfunction)
        for function in functions:
            assert len(re.findall('([A-Z])', function[0])) == 0, "You have used Capital letter(s) in your function names"

def test_iterable():
    #T1: PolygonSeqType is Iterable
    poly = PolygonSeqType(5, 6)
    assert '__iter__' in dir(poly), 'PolygonSeqType supposed to be Iterable'

    #T2: PolygonSeqType 
    assert iter(poly) is not poly, 'Iterable should return an iterator but not self'

    #T3: Iterable should not be exhaustible
    try:
        for index in range(5):
            for index in range(len(poly)):
                poly[index]
    except StopIteration:
        assert False, ('Iterable is not expected to be exhausted, however have received the StopIteration exception ')

def test_iterator():
    #T4: PolygonSeqType contains iterator
    poly = PolygonSeqType(5, 6)
    iter_1 = iter(poly)
    assert '__iter__' in dir(iter_1), 'PolygonSeqType Should contain __iter__ function'
    assert '__next__' in dir(iter_1), 'PolygonSeqType Should contain __next__ function'

    #T5: Iterator returns self
    poly_iter = iter(poly)
    poly_iter_1 = iter(poly_iter)
    assert poly_iter == poly_iter_1, 'Iterator should return self, something went wrong!'

    #T6: Iterator should be exhaustible
    for index in range(len(poly)):
        next(iter_1)
    try:
        next(iter_1)
        assert False, ('Iterator is expected to be exhausted, however have not received the StopIteration exception ')
    except StopIteration:
        pass

def test_sequence_type():
    #T7: PolygonSeqType is sequence type
    poly = PolygonSeqType(5, 6)
    assert '__getitem__' in dir(poly), 'PolygonSeqType supposed to be Sequence Type too'

    #T8: PolygonSeqType is subscriptable
    for index in range(len(poly)):
        try:
            poly[index]
        except TypeError:
            assert False, ('PolySeqType is a sequence type and should support indexing')