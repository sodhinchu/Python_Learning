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
    "Sequence",
    "index",
    "polygon",
    "repr",
    "len",
    "getitem",
    "area",
    "perimeter",
    "edge",
    "edges",
    "vertices",
    "radius",
    "circumradius",
    "equality",
    "greater",
    "interior angle",
    "apothem",
    'max efficiency'
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

def test_polygon():
    #T1: Check for invalid input parameters
    with pytest.raises(AttributeError) as execinfo:
        Polygon(edges=2, radius = 5)

    with pytest.raises(AttributeError) as execinfo:
        Polygon(edges=3, radius = -5)

    with pytest.raises(AttributeError) as execinfo:
        Polygon(edges=2, radius = -5)

    #T2: Cheeck for valid Polygon creation and its __repr__() function
    p1 = Polygon(edges=4, radius=7)
    assert('edges' in p1.__repr__() and 'radius' in p1.__repr__())

    #T3: Check for equality based on edges and circumradius
    p1 = Polygon(edges=4, radius=7)
    p2 = Polygon(edges=4, radius=7)
    assert(p1 == p2), 'Polygons should be equal'

    p1 = Polygon(edges=4, radius=7)
    p2 = Polygon(edges=14, radius=7)
    assert(p1 != p2), 'Polygons should not be equal'

    #T4: Check for greater than based on edges
    p1 = Polygon(edges=14, radius=7)
    p2 = Polygon(edges=4, radius=7)
    assert(p1 > p2), 'P1 should be greater than P2'

    #T5: Check for accessing the members
    edges = 3
    radius = 6
    p1 = Polygon(edges, radius)
    assert(p1.edges == edges), 'Edges should be matching'
    assert(p1.radius == radius), 'Radius should be matching'
    assert(p1.angle == 60), 'Angle should be matching'

def test_polygon_seqtype():
    #T1: Check for invalid input parameters
    with pytest.raises(AttributeError) as execinfo:
        PolygonSeqType(max_edges=2, common_radius = 5)

    with pytest.raises(AttributeError) as execinfo:
        PolygonSeqType(max_edges=3, common_radius = -5)

    with pytest.raises(AttributeError) as execinfo:
        PolygonSeqType(max_edges=2, common_radius = -5)

    #T2: Check for valid Polygon creation and its __repr__() function
    max_edges = 4
    common_radius = 4
    p1 = PolygonSeqType(max_edges, common_radius)
    assert('max_edges' in p1.__repr__() and 'common_radius' in p1.__repr__())

    #T3: Get the max polygon length
    assert(len(p1) == (max_edges - 2)), 'Number of Polygons available is not matching!'

    #T4: Get next polygon in a loop
    # (internally __getitem__() gets called for each time accessing p1 with index
    num_poly = p1.__len__()
    for index in range(num_poly):
        poly = p1[index]
        assert(poly.edges == index+3 and poly.radius == common_radius), 'Edges and Radius values not matching'

    #T5: Validate Slicing
    max_edges = 10
    common_radius = 40
    #Creates multiple polygons with edges ranging from 3 to 10 [indexed from 0 to 7]
    p1 = PolygonSeqType(max_edges, common_radius)
    # Should return the polygon from index 2 to 5(excluding 5) = Polygon(edges=5), Polygon(edges=6), Polygon(edges=7) 
    p_slice = p1[2:5]
    assert(p_slice[0].edges == 5 and p_slice[1].edges == 6 and
            p_slice[2].edges == 7 and p_slice[0].radius == common_radius), 'Slicing didn\'t work as expected'
    # Should return the polygon from index 21 to 40(excluding 40)
    # Polygons available from index 0 to 7 [Total of 8 length] - Should return Polygon(edges=9), Polygon(edges=10)
    p_slice = p1[6:40]
    assert(p_slice[0].edges == 9 and p_slice[1].edges == 10 and
            p_slice[0].radius == common_radius and p_slice[1].radius == common_radius), 'Slicing didn\'t work as expected'

    #T6: Check for max efficiency polygon
    max_edges = 25
    common_radius = 34
    p1 = PolygonSeqType(max_edges, common_radius)
    assert(p1.max_efficient_polygon().edges == max_edges), 'Mismatch in the calculation of Max Efficient Polygon'