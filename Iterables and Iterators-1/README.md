# Iterables and Iterators-1
Repeating a set of instructions (or a code block or a dataset) multiple times is called iteration.<br/>
**while**, **for** are two basic loops that enable iterate over a set of instructions.<br/>
A traditional **for** loop contains the index with some starting value, a condition and action at end of each iteration.<br/>
```bash
for i = 0; i < 10; i++
	<code block>
```
<br/>
Python **for** loop differs from the above mentioned looping.<br/>
The initialization and condition are clubbed in an iterable and the looping stops (automatically) when the elements are over.<br/>
```bash
for <item> in <iterable>:
	<code block>
```
<br/>
Python supports multiple built-in iterables lists, tuples, sets, dictionaries and strings.<br/>
For all these iterables, **for** loop can be used to iterate through the elements<br/>

### Iterator
1. Iterator is a class whose **__iter__** method returns self<br/>
2. Iterator must support **__next__** method that helps in accessing next element from the collections<br/>
3. Iterator exhausts after reaching te last element in the collection and throws StopIteration Exception<br/>
4. Iterator doesn't support indexing and do not have length<br/>
5. With **__iter__** implementation, **for** loop can be used to iterate through collection
```bash
**Iterator can be obtained from an iterable like below**
l = [1, 2, 3]
iter_1 = iter(l)
iter_2 = iter(iter_1)

Since Iterator its self, below statement returns True
>> iter_1 is iter_2
True

>> next(iter_1)
1
>> next(iter_1)
2
>> next(iter_1)
3
>> next(iter_1)
StopIteration Exception
```

### Iterable
1. Iterable is a class whose **__iter__** method returns an iterator
2. Iterable may support (optional) **__next__** method for looping
3. Iterable never exhausts and can be looped through all the elements over and over again
4. Iterable supports indexing (and slicing) by implementing the method **__getitem__**

### Creating Custom Iterator
For building custom dataloaders, custom iterators come in handy. A class with the methods **__iter__**, **__next_** can act as Custome Iterator <br/>
A class without **__iter__** method implementation cannot be iterated over using **for** loop <br/>

### Creating Custom Iterable
Since an iterator (with __iter__, __next__ methods) exhausts churning out items after one iteration. There needs to be a way to loop over multiple times and keep creating the iterator object each time. Thats where the custom iterables come into picture <br/>
Custom iterable implements the method **__iter__** <br/>
**__iter__** method of iterable returns an iterator (see above for understanding more about iterator) <br/>
With this implementationm now the class becomes iterable and can be looped over using **for** loop <br/>
All Sequences are Iterables but the inverse is not always true. To convert the iterable class to sequnce type, implement the method **__getitem__** <br/>

**__getitem** method enables the class objects to be subscribable and with slicing implementation inside the **__getitem__** method, the object can be slicable as well <br/>

```bash
Following is an example custom iterator that generates numbers in a given range
class gen_numbers:
	def __init__(self, min_val, max_val1):
		self.min_val = min_val
		self.max_val = max_val
		self.index = min_val

	def __iter__(self):
		return self

	def __next__(self):
		if(self.index >= self.max_val):
			raise StopIteration
		else:
			num = self.index
			self.index += 1
			return num

>> numbers = gen_numbers(1, 3)
>> next(numbers)
1
>>  next(numbers)
2
>> next(numbers)
StopIteration Exception
```
### Project Work
Refactor the Polygons (sequence) type, into an iterable. You'll need to implement both an iterable, and an iterator.<br/>
