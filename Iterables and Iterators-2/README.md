# Iterables and Iterators - 2
This Session continues over the previous understanding of Iterables and Iterators.<br/>
A quick recap of Iterables and Iterators is given below.<br/>
<br/>
Repeating a set of instructions (or a code block or a dataset) multiple times is called iteration.<br/>
<br/>
Python supports multiple built-in iterables lists, tuples, sets, dictionaries and strings.<br/>
For all these iterables, **for** loop can be used to iterate through the elements<br/>
<br/>
### Iterator
1. Iterator is a class whose **__iter__** method returns self<br/>
2. Iterator must support **__next__** method that helps in accessing next element from the collections<br/>
3. Iterator exhausts after reaching te last element in the collection and throws StopIteration Exception<br/>
4. Iterator doesn't support indexing and do not have length<br/>
5. With **__iter__** implementation, **for** loop can be used to iterate through collection <br/>
<br/>
### Iterable
1. Iterable is a class whose **__iter__** method returns an iterator<br/>
2. Iterable may support (optional) **__next__** method for looping<br/>
3. Iterable never exhausts and can be looped through all the elements over and over again<br/>
4. Iterable supports indexing (and slicing) by implementing the method **__getitem__**<br/>
<br/>
### Custom Iterator
For building custom dataloaders, custom iterators come in handy. A class with the methods **__iter__**, **__next_** can act as Custome Iterator <br/>
A class without **__iter__** method implementation cannot be iterated over using **for** loop <br/>
<br/>
### Custom Iterable
Since an iterator (with __iter__, __next__ methods) exhausts churning out items after one iteration. There needs to be a way to loop over multiple times and keep creating the iterator object each time. That's where the custom iterables come into the picture <br/>
Custom iterable implements the method **__iter__** <br/>
**__iter__** method of iterable returns an iterator (see above for understanding more about iterator)<br/>
With this implementation now the class becomes iterable and can be looped over using **for** loop<br/>
<br/>

### Lazy Loading
Many-a-times a class has multiple properties of which not all properties are needed at all times. Some of these properties occupy considerable RAM as well. Is there a more Pythonic way to handle this requirement of compute these properties only when required? <br/>
Lazy loading can be supported for attributes, for module imports, for caching values and many more<br/>

The lazy loading has multiple advantages<br/>
1. Reduces loading time:<br/>
Instead of computing all the attributes in class, this helps computing them only when accessed thus reduces the time during class initialization
2. Bandwidth conservation:<br/>
If the code uses downloading of any data for its attributes computation, lazy loading helps downloading content only when that particular attribute/method is accessed rather than consuming all the bandwidth irrespective of its actual usage in the class
3. Efficient use of System Resources:<br/>
For heavy datasets, reading the whole file contents consumes up complete RAM and may crash the system if the RAM is not big enough to hold the data. In such cases, loading only the necessary contents (line by line, few bytes of data) can ease up system resources and doesn't cause overloading of the system

Python has **property** annotator that replicates the above behaviour, computing the attributes only when they are accessed<br/>
The **property** annotator enables <br/>
1. Class attributes to be accessed like public attributes <br/>
2. Sets restrictions on assigning new values from outside the class(by user) or by other methods<br/>
3. Can reuse the name of the property to avoid creating new names for the getters, setters and deleters <br/>

### Caching Data
The lazy loading coupled with caching(immutable class) reduces further computation as the variables won't be computed if they are already availabl.<br/>
This behaviour can be obtained by setting the attributes to None during setters of mandatory attributes and once computed continue using the same value without subsequent computations.<br/>

### Project Work
#### Goal 1:
Refactor the Polygon class so that all the calculated properties are lazy properties, i.e. they should still be calculated properties, but they should not have to get recalculated more than once (since we made our Polygon class "immutable").<br/>
#### Goal 2:
Refactor the Polygons (sequence) type, into an iterable. Make sure also that the elements in the iterator are computed lazily - i.e. you can no longer use a list as an underlying storage mechanism for your polygons.<br/>
You'll need to implement both an iterable, and an iterator.<br/>

Notebook for the assignment is https://colab.research.google.com/drive/1KdandogUoYxLsRirYFE0lxa0xQ9tndY8#scrollTo=WtXHvaEq0ZOM <br/>

### Class Overview
#### Polygon
Polygon is a class which takes edges, radius as inputs and computes its necessary properties (like area, perimeter, angle etc.) <br/>
A valid polygon have edges as minimum as 3 and a non-zero, non-negative radius<br/>
The Class supports getters and setters for edges, radius using @property annotation<br/>
The Class also supports lazy computing of its properties and also the properties are not claculated more than once<br/>

#### PolygonSeqType
PolygonSeqType is an Iterable which allows to iterate through list of polygons with its own custom iterator<br/>
The iterable also supports lazy loading of its attributes such as the polygon list and the maximum efficiency polygon attributes<br/>
