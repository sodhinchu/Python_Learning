from math import pi, sin, cos
from collections import namedtuple

class Polygon:
    '''
    Polygon is a class which takes edges, radius as inputs and computes its necessary properties (like area, perimeter, angle etc.)
    A valid polygon have edges as minimum as 3 and a non-zero, non-negative radius

    The Class supports getters and setters for edges, radius using @property annotation
    The Class also supports lazy computing of its properties and also the properties are not claculated more than once
    '''
    def __init__(self, edges, radius):
        self.edges = edges
        self.radius = radius

    @property
    def edges(self):
        return self._edges

    @edges.setter
    def edges(self, edges):
        if(edges < 3 or not isinstance(edges, int)):
            raise AttributeError(f'Invalid Input values in object creation, Cross check: edges: {edges}')
            return
        self._edges = edges
        #Initializing the properties every time a new value is set for edges
        self._angle = None
        self._apothem = None
        self._area = None
        self._edgelen = None
        self._perimeter = None

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, radius):
        if(radius <= 0 or not isinstance(radius, int)):
            raise AttributeError(f'Invalid Input values in object creation, Cross check: radius: {radius}')
            return

        self._radius = radius
        #Initializing the properties every time a new value is set for radius
        self._angle = None
        self._apothem = None
        self._area = None
        self._edgelen = None
        self._perimeter = None

    @property
    def angle(self):
        '''
        Checks if angle is already computed
        If not, computes angle using the formula and returns the value
        If so, returns the available value
        '''
        if self._angle is None:
            print('Computing Angle')
            n = self._edges
            self._angle = (n - 2) * (180/n)
        else:
            print('Using Cached Value for Angle')
        return self._angle

    @property
    def edgelen(self):
        '''
        Checks if edge_len is already computed
        If not, computes edge_len using the formula and returns the value
        If so, returns the available value
        '''
        if self._edgelen is None:
            print('Computing EdgeLen')
            self._edgelen = (2 * self._radius * sin(pi)/self._edges)
        else:
            print('Using Cached Value for EdgeLen')
        return self._edgelen

    @property
    def apothem(self):
        '''
        Checks if apothem is already computed
        If not, computes apothem using the formula and returns the value
        If so, returns the available value
        '''
        if self._apothem is None:
            print('Computing Apothem')
            self._apothem = (self._radius * cos(pi)/self._edges)
        else:
            print('Using Cached Value for Apothem')
        return self._apothem

    @property
    def area(self):
        '''
        Checks if area is already computed
        If not, computes area using the formula and returns the value
        If so, returns the available value
        '''
        if self._area is None:
            print('Computing Area')
            #Since area requires edge_len, apothem in the formula, the values should be available
            if self._edgelen is None:
                self._edgelen = self.edgelen

            if self._apothem is None:
                self._apothem = self.apothem

            self._area = (self._edges * self._edgelen * self._apothem)/float(2)
        else:
            print('Using Cached Value for Area')
        return self._area

    @property
    def perimeter(self):
        '''
        Checks if perimeter is already computed
        If not, computes perimeter using the formula and returns the value
        If so, returns the available value
        '''
        if self._perimeter is None:
            print('Computing Perimeter')
            if self._edgelen is None:
                self._edgelen = edgelen()
            self._perimeter = (self._edges * self._edgelen)
        else:
            print('Using Cached Value for Perimeter')
        return self._perimeter

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