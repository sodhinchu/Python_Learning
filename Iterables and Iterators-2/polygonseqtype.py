from polygon import Polygon

class PolygonSeqType:
    '''
    PolygonSeqType is a class which takes max_edges, common_radius as inputs and supports iterating through \
    list of polygons and also has max_efficient_polygon property which indicates the maximum efficient polygon in the list
    A valid polygon have edges as minimum as 3 and a non-zero, non-negative radius

    The Class supports getters and setters for max_edges, common_radius using @property annotation
    The Class also supports lazy computing of its properties and also the properties are not claculated more than once
    '''
    def __init__(self, max_edges, common_radius):
        self.maxedges = max_edges
        self.commonradius = common_radius

    @property
    def maxedges(self):
        #Getter for maxedges
        return self._maxedges

    @maxedges.setter
    def maxedges(self, max_edges):
        #Validate input values
        if(max_edges <= 2 or not isinstance(max_edges, int)):
            raise AttributeError(f'Invalid Input values in object creation, Cross check: max_edges:{max_edges}')
        else:
            #Setter for maxedges
            self._maxedges = max_edges
            self._polygons = []
            self._maxpolygon = None

    @property
    def commonradius(self):
        #Getter for CommonRadius
        return self._commonradius

    @commonradius.setter
    def commonradius(self, common_radius):
        #Validate Input Values
        if(common_radius <= 0 or not isinstance(common_radius, int)):
             raise AttributeError(f'Invalid Input values in object creation, Cross check: common_radius: {common_radius}')
        else:
            #Setter for CommonRadius
            self._commonradius = common_radius
            self._polygons = []
            self._maxpolygon = None

    def __len__(self):
        return (self._maxedges-2)

    def __iter__(self):
        #Iterable returning an iterator
        return self.PolygonIterator(self)

    def __getitem__(self, p):
        #Required for Subscription
        if(isinstance(p, int)):
            if(p < 0):
                #To support reverse iteration l[-1], [-2]...
                p = p + self.__len__()
            if(p < 0 or p >= self.__len__()):
                raise IndexError(f'Index {p} is out of range, maximum length {self.__len__()}')
            else:
                #Checks if Polygon for the query index is already available, if so returns the same
                #If not, computes the Polygon and returns the computed value
                try:
                    print('Using Cached Value of Polygon for the query index')
                    polygon = self._polygons[p]
                except IndexError:
                    print('Computing Polygon for the query index')
                    polygon = self._create_polygon(p)
                    self._polygons.append(polygon)
                return polygon
        else:
            #This is to support slicing
            start, stop, step = p.indices(self.__len__())
            rng = range(start, stop, step)
            poly_slices = []
            for index in rng:
                try:
                    #Checks if Polygon for the query index is already available, if so returns the same
                    #If not, computes the Polygon and returns the computed value
                    print('Using Cached Value of Polygon for the query index')
                    poly_slices.append(self._polygons[index])
                except IndexError:
                    print('Computing Polygon for the query index')
                    self._polygons.append(self._create_polygon(p))
                    poly_slices.append(self._polygons[index])
            return poly_slices

    def _create_polygon(self, index):
        '''
        This is an internal function to create a new polygon
        Also resets the value of MaxPolygon as its value will be changed with addition of every new polygon
        '''
        self._maxpolygon = None
        return Polygon(index+3, self._commonradius)

    @property
    def maxpolygon(self):
        '''
        Computes maximum efficiency polygon
        Maximum Efficiency = Polygon with highest area to perimeter ratio
        '''
        if self._maxpolygon is None:
            #Checks if MaxPolygon is already computed, if so returns the cached value
            #If not computes and returns the value
            print('Computing MaxPolygon')

            #Inorder to calculate MaxPolygon, the Polygon List has to be available
            #If it is not available, first create the polygon list and then compute MaxPolygon value
            poly_len = len(self._polygons)
            max_poly_len = self.__len__()

            if(poly_len != max_poly_len):
                for index in range(poly_len, max_poly_len):
                    print('Computing Polygon for the query index')
                    self._polygons.append(self._create_polygon(index))

            sorted_polygons = sorted(self._polygons, key=lambda p: p.area/p.perimeter, reverse=True)
            self._maxpolygon = sorted_polygons[0]
        else:
            print('Using Cached Value for MaxPolygon')
        return self._maxpolygon

    def __repr__(self):
        return(f'PolygonSeqType(max_edges = {self._maxedges}, common_radius = {self._commonradius})')

    class PolygonIterator:
        '''
        Iterator Class that allows looping through the collection
        '''
        def __init__(self, polyobj):
            #Save PolygonSeqType object for access during iterations/next item fetch
            self._index = 0
            self._polyobj = polyobj

        def __iter__(self):
            #Iterator returning self
            return self

        def __next__(self):
            '''
            __next__() function to fetch elements one by one
            Since the Polygons list is not created in advance, every time a call is made to acces next element
            Only that time, the polygon is created and maintained in the list
            Once all the Polygons are computed the list is reused and won't be created again and again in subsequent iter calls
            This way the iterator supports lazy computation of Polygons Data
            '''
            if self._index >= self._polyobj.__len__():
                raise StopIteration
            else:
                try:
                    print('Using Cached Value of Polygon for the query index')
                    polygon = self._polyobj._polygons[self._index]
                except IndexError:
                    print('Computing Polygon for the query index')
                    polygon = self._polyobj._create_polygon(self._index)
                    self._polyobj._polygons.append(polygon)
                self._index += 1
                return polygon