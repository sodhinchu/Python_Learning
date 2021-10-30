from math import pi, sin, cos
from collections import namedtuple

class Polygon:
    def __init__(self, edges, radius):
        if(edges < 3 or radius <= 0 or not isinstance(edges, int) or not isinstance(radius, int)):
            raise AttributeError(f'Invalid Input values in object creation, Cross check: edges: {edges}/radius: {radius}')
            return
        #Create Polygon objects with the input arguments edges and radius
        self.edges = edges
        self.vertices = edges
        self.radius = radius
        #Compute the properties (area, perimeter, angle, apothem etc.) of Polygon
        self._compute_properties()

    def getedges(self):
        return self.edges

    def getvertices(self):
        return self.vertices

    def getcircumradius(self):
        return self.radius

    def _calcinteriorangle(self):
        n = self.getedges()
        self.angle = (n - 2)  * (180/n)
        return self.angle

    def _calcedgelength(self):
        self.edgelen = (2 * self.getcircumradius() * sin(pi)/self.getedges())
        return self.edgelen

    def _calcapothem(self):
        self.apothem = (self.getcircumradius() * cos(pi)/self.getedges())
        return self.apothem

    def _calcarea(self):
        self.area = (self.edges * self.edgelen * self.apothem)/float(2)
        return self.area

    def _calcperimeter(self):
        self.perimeter = (self.edges * self.edgelen)
        return self.perimeter

    def _compute_properties(self):
        #Calculates angle, edge length, apothem, area and perimeter for the Polygon
        self._calcinteriorangle()
        self._calcedgelength()
        self._calcapothem()
        self._calcarea()
        self._calcperimeter()

    def __repr__(self):
        return(f'Polygon(edges={self.edges}, radius={self.radius})')

    def __eq__(self, p):
        '''
        Implements Equality operation
        Validates whether the input object is of type Polygon or not
        If so checks whether edges and radius both are matching. Returns True if both are matching else returns False
        '''

        if(isinstance(p, Polygon)):
            if(p.edges == self.edges and p.radius == self.radius):
                return True
            else:
                return False
        else:
            raise TypeError(f'\'==\' not supported between instances of \'Polygon\' and {type(p)}')

    def __gt__(self, p):
        '''
        Implements Greater than operation
        Validates whether the input object is of type Polygon or not
        If so checks whose edges are higher and returns True/False based on that
        '''
        if(isinstance(p, Polygon)):
            if(self.edges > p.edges):
                return True
            else:
                return False
        else:
            raise TypeError(f'\'>\' not supported between instances of \'Polygon\' and {type(p)}')