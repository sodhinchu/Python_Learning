from polygon import Polygon

class PolygonSeqType:
    def __init__(self, max_edges, common_radius):
        if(max_edges <= 2 or common_radius <= 0 or not isinstance(max_edges, int) or not isinstance(common_radius, int)):
            raise AttributeError(f'Invalid Input values in object creation, Cross check:\
                                    max_edges:{max_edges} / common_radius: {common_radius}')
            return
        self._edges = max_edges
        self._radius = common_radius
        #Create Polygon objects with the input arguments edges and radius
        #A list of polygons are created with edges = 3 till the maximum edges input
        self._polygons = [Polygon(index, self._radius) for index in range(3, max_edges+1)]
        self._index = 0

    def __len__(self):
        return (self._edges-2)

    def __iter__(self):
        #Iterable returning an iterator
        return self.PolygonIterator(self)

    def __getitem__(self, p):
        if(isinstance(p, int)):
            if(p < 0):
                #To support reverse iteration l[-1], [-2]...
                p = p + self.__len__()
            if(p < 0 or p >= self.__len__()):
                raise IndexError(f'Index {p} is out of range, maximum length {self.__len__()}')
            else:
                #Returns pth polygon from the list
                return self._polygons[p]
        else:
            '''
            This is to support slicing
            '''
            start, stop, step = p.indices(self.__len__())
            rng = range(start, stop, step)
            return [self._polygons[index] for index in rng]

    def max_efficient_polygon(self):
        '''
        Computes maximum efficiency polygon
        Maximum Efficiency = Polygon with highest area to perimeter ratio
        '''
        poly_area = []
        poly_perimeter = []
        # Iterate over all the available polygons
        for index in range(self.__len__()):
            # Extract area, perimeter values for each polygon
            polygon = self._polygons[index]
            poly_area.append(polygon.area)
            poly_perimeter.append(polygon.perimeter)
        # Compute area to perimeter ratio for each polygon
        poly_efficient = [area/float(perimeter) for area, perimeter in zip(poly_area, poly_perimeter)]
        #Out of all polygons, return the polygon with highest area to perimeter ratio
        return self._polygons[poly_efficient.index(max(poly_efficient))]

    def __repr__(self):
        return(f'PolygonSeqType(max_edges = {self._edges}, common_radius = {self._radius})')

    class PolygonIterator:
        '''
        Iterator Class that allows looping through the collection
        '''
        def __init__(self, polyobj):
            #Save PolygonSeqType object for access during iterations/next item fetch
            self._index = 0
            self._poly_obj = polyobj

        def __iter__(self):
            #Iterator returning self
            return self

        def __next__(self):
            #Fetching elements one by one
            if self._index >= len(self._poly_obj):
                raise StopIteration
            else:
                polygon = self._poly_obj._polygons[self._index]
                self._index += 1
                return polygon