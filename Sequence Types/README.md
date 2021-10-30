# Sequence Types
Sequences are collection of items that support accessing its elements using indexing. <br/>
Below is an example of what a sequence is <br/>
```bash
S = x0, x1, x2, ....
x1 can be accessed as S[1], second element in the sequence
```
<br/>
Python supports number of built-in sequence types that are mutable and immutable <br/>
Lists are mutable sequence types, whereas strings, tuples come under immutable sequence types <br/>
Some of the sequence types support heterogenous data and some only support homegenous data <br/>

```bash
#List sequence type: Heterogeneous data
l1 = [1, 2.3, 'python']

#String sequence type: Homegeneous data
str1 = 'tsai'
```
<br/>
Sequence types in Python have another property and they support iteration <br/>
All sequence types are iterables but the inverse is not always true <br/>

```bash
#List sequence type: Shows Iteratability along with indexing
l1 = [1, 2.3, 'python']
for index in l1:
	print(l1[index]) -->> Prints each element in list l1

#Iterable but not Sequence type
k1 = {1, 2, 3}
for ele in k1:
	print(ele) -->> Each element can be accessed in iteration
But k1[0] -->> Throws error (Indexing Not supported)
```
<br/>
Built-in sequence types in Python supports various methods to access/perform operations on its elements <br/>

```bash
#List sequence type
l1 = [1, 4, 5, 1]
len(l1) -> Length of the list = 4
1 in l1 -> Checks if 1 is in list and returns True if available
4 not in l1 -> Checks if 4 not in list and returns False for the example
min(l1) -> Minimum element in the list = 1
max(l1) -> Maximum element in the list = 5
l1.index(1) -> Returns the index where the element 1 occurs in the list = 0
l1.index(1, 0) -> Returns the index of first occurence of 1 in l1 at or after index 0 = 0
l1.index(1, 2) -> Returns the index of first occurence of 1 in l1 at or after index 2 = 3
l1.index(1, 0, 3) -> Returns the index of first occurence of 1 in l1 at or after index 0 and before index 3 = 0
```
<br/>
Slicing: Python Sequene types support Slicing which aids in accessing the elements using various conditions <br/>

```bash
#List sequence type
l1 = [1, 4, 5, 1]
l1[0:2] -->> Returns the list which includes elements from index (0) till index (2) by excluding it = [1, 4]
l1[0:4:2] -->> Extended slice from index (0), but not including (4), in steps of (2) = [1, 5]
```
<br/>
Custom Sequence Types: These are Python classes with additional functionality starts behaving like a sequence type (meaning: supports indexing, iterating, slicing, isinstance etc.) <br/>
This type of functionality is require to write custom dataloaders for loading data from corpus <br/>
For a python class to start working as sequence type, it should implement the methods: __getitem__(), __len__() <br/>

```bash
Below is a sample class which implements __len__(), __getitem__() methods and
supports slicing, indexing and iterating for the caller

class cs1:
	def __init__(self, n):
		self.n = n
		self.items = [i for i in range(n)]

	def __len__(self):
		return self.n

	def __getitem__(self, x):
		if(isinstance(x, int)):
			if x < 0:
				x = x + self.n
			if x < 0 or x >= self.n:
				raise IndexError
			else:
				return self.items[x] #returns 'x' th element
		else:
			start, stop, step = x.indices(self.n)
			rng = range(start, stop, step)
			return [self.items(i) for i in rng]
```

## Project Work
1. Create a Polygon Class, where initializer takes in: number of edges/vertices, circumradius <br/>
2. Polygon Class should have the properties: # edges, # vertices, interior angle, edge length, apothem, area and perimeter <br/>
3. The Polygon Class should support the functionality: proper __repr__ function, (__eq__) based on # vertices and circum radius, (__gt__) based on number of vertices only <br/>
4. Implement a Custom Polygon sequence type, where initializer takes in number of vertices for largest polygon in the sequence, common circumradius for all polygons <br/>
5. Polygon SeqType should have the properties: max efficiency polygon: returns the Polygon with the highest area: perimeter ratio <br/>
6. Polygon SeqType should support the functionality: __getitem__(), __len__(), proper representation (__repr__)
