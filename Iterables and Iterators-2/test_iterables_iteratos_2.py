import pytest
import sys
import inspect
import os
import re
from io import StringIO 

import polygon
from polygon import Polygon
import polygonseqtype
from polygonseqtype import PolygonSeqType

README_CONTENT_CHECK_FOR = [
    "Iterable",
    "Iterator",
    "__iter__",
    "__next__",
    "__getitem__",
    "iteration",
    "indexing",
    "for",
    "StopIteration",
    "exhausts",
    "custom",
    "lazy",
    "caching",
    "property",
    "immutable"
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

def test_lazy_property_polygon():
    #T9: All the properties should be lazily computed (Meaning unless they are accessed, they won't be computed)
    #One method to verify this behaviour is to check the dictionary of the object
    #If the values are not available, they are assigned to None, if the values are computed they will have non-None values
    #Comparing the values against None and not None gives us understanding whether the value is computed and when it is computed
    poly = Polygon(5, 6)

    #The object for Polygon Class is created above, and no call made for its properties
    #If the class supports lazy loading, the properties should be equal to None
    assert poly.__dict__['_angle'] is None, 'Angle is available already, Un-necessarily active!'
    assert poly.__dict__['_edgelen'] is None, 'EdgeLen is available already, Un-necessarily active!'
    assert poly.__dict__['_apothem'] is None, 'Apothem is available already, Un-necessarily active!'
    assert poly.__dict__['_area'] is None, 'Area is available already, Un-necessarily active!'
    assert poly.__dict__['_perimeter'] is None, 'Perimeter is available already, Un-necessarily active!'

    #T10: Now compute angle, edgelen, apothem, area, perimeter and verify one more time
    #Since the properties are accessed, the values should be non None
    poly.angle
    assert poly.__dict__['_angle'] is not None, 'Angle is still not available in dictionary, Recheck your logic!'
    poly.edgelen
    assert poly.__dict__['_edgelen'] is not None, 'EdgeLen is still not available in dictionary, Recheck your logic!'
    poly.apothem
    assert poly.__dict__['_apothem'] is not None, 'Apothem is still not available in dictionary, Recheck your logic!'
    poly.area
    assert poly.__dict__['_area'] is not None, 'Area is still not available in dictionary, Recheck your logic!'
    poly.perimeter
    assert poly.__dict__['_perimeter'] is not None, 'Perimeter is still not available in dictionary, Recheck your logic!'


def test_setter_error_prop_polygon():
    #T11: The properties should not be used for setting new values from outside
    #One method to verify this behaviour is to try assigning to new value and check if AttributeError is raised

    poly = Polygon(5, 6)
    with pytest.raises(AttributeError) as execinfo:
        poly.angle = 180

    with pytest.raises(AttributeError) as execinfo:
        poly.edgelen = 15

    with pytest.raises(AttributeError) as execinfo:
        poly.apothem = 51

    with pytest.raises(AttributeError) as execinfo:
        poly.area = -10

    with pytest.raises(AttributeError) as execinfo:
        poly.perimeter = 105


def test_lazy_property_polygonseqtype():
    #T12: The properties should be lazily computed (Meaning unless they are accessed, they won't be computed and will be equal to None)
    poly = PolygonSeqType(5, 6)
    assert poly.__dict__['_maxpolygon'] is None, 'MaxEfficient Polygon is available already, Un-necessarily active!'
    assert len(poly.__dict__['_polygons']) == 0, 'Complete Polygons List is available already, Un-necessarily active!'
    #At start, the polygons list should be empty and accessing its elements should raise IndexError
    with pytest.raises(IndexError) as execinfo:
        poly._polygons[0]

    #T13: Now compute angle, edgelen, apothem, area, perimeter and verify one more time
    #Since the properties are accessed, the values should be non None
    poly_iter = iter(poly)
    next(poly_iter)
    assert len(poly.__dict__['_polygons']) == 1, 'Complete Polygons List is available already, Un-necessarily active!'
    next(poly_iter)
    assert len(poly.__dict__['_polygons']) == 2, 'Complete Polygons List is available already, Un-necessarily active!'
    poly.maxpolygon
    assert poly.__dict__['_maxpolygon'] is not None, 'MaxEfficient Polygon is still not available in dictionary, Recheck your logic!'
    assert len(poly.__dict__['_polygons']) == len(poly), 'Complete Polygons List is still not available in dictionary, Recheck your logic!'


def test_setter_error_prop_polygonseqtype():
    #T14: The properties should not be used for setting new values from outside
    #One method to verify this behaviour is to try assigning to new value and check if AttributeError is raised

    poly = PolygonSeqType(5, 6)

    with pytest.raises(AttributeError) as execinfo:
        poly.maxpolygon = Polygon(7, 6)

class Capturing(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self
    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio    # free up some memory
        sys.stdout = self._stdout

def test_cached_property_polygon():
    #T15: The Lazy Property means the values are not computed unless they are accessed and also if the value is computed once, won't be recomputed multiple times
    #One way to verify the behaviour is by scanning the print statements generated during the computation
    #If the value is computed, the stdout contains the print of Computed
    #If the value is reused, the stdout contains the print of Cached
    poly = Polygon(5, 6)

    # assert if Computing and the Property Name are not matching in Output
    with Capturing() as output:
        poly.edgelen
    assert any(["Computing" and "EdgeLen" in o for o in output])

    # assert if Cached and the Property Name are not matching in Output
    with Capturing() as output:
        poly.edgelen
    assert any(["Cached" and "EdgeLen" in o for o in output])

    # assert if Computing and the Property Name are not matching in Output
    with Capturing() as output:
        poly.angle
    assert any(["Computing" and "Angle" in o for o in output])

    # assert if Cached and the Property Name are not matching in Output
    with Capturing() as output:
        poly.angle
    assert any(["Cached" and "Angle" in o for o in output])

    # assert if Computing and the Property Name are not matching in Output
    with Capturing() as output:
        poly.apothem
    assert any(["Computing" and "Apothem" in o for o in output])

    # assert if Cached and the Property Name are not matching in Output
    with Capturing() as output:
        poly.apothem
    assert any(["Cached" and "Apothem" in o for o in output])

    # assert if Computing and the Property Name are not matching in Output
    with Capturing() as output:
        poly.area
    assert any(["Computing" and "Area" in o for o in output])

    # assert if Cached and the Property Name are not matching in Output
    with Capturing() as output:
        poly.area
    assert any(["Cached" and "Area" in o for o in output])

    # assert if Computing and the Property Name are not matching in Output
    with Capturing() as output:
        poly.perimeter
    assert any(["Computing" and "Perimeter" in o for o in output])

    # assert if Cached and the Property Name are not matching in Output
    with Capturing() as output:
        poly.perimeter
    assert any(["Cached" and "Perimeter" in o for o in output])

def test_cached_property_polygonseqtype():
    #T16: The Lazy Property means the values are not computed unless they are accessed and also if the value is computed once, won't be recomputed multiple times
    #One way to verify the behaviour is by scanning the print statements generated during the computation
    #If the value is computed, the stdout contains the print of Computed
    #If the value is reused, the stdout contains the print of Cached
    poly = PolygonSeqType(5, 6)

    with Capturing() as output:
        poly.maxpolygon

    # assert if Computing and the Property Name are not matching in Output
    assert any(["Computing" and "MaxPolygon" in o for o in output])
    assert any(["Computing" and "Polygon" in o for o in output])

    with Capturing() as output:
        poly.maxpolygon

    # assert if Cached and the Property Name are not matching in Output
    assert any(["Cached" and "MaxPolygon" in o for o in output])
    assert any(["Cached" and "Polygon" in o for o in output])