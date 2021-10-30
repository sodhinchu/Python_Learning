# Generators and Iteration Tools
Generators are python functions that enable a function to behave like an iterator.<br/>
By adding **__iter__**, **__next__** functions a class can become an iterator. Generators offer the same functionality without the burden of creating a class, taking care of state maintenance. Also the generators offer lazy loading of data.<br/>
The difference between a function and a generator function is the presence of **yield** in the place of **return**.<br/>
Another key difference is: Generator functions don't even run the function, rather creates and returns a generator object. The code inside generator functions gets executed only when **next()** is called on the generator object<br/>
<br/>
The iterator functionality of Generators enable function to loop over like **lists**. They offer the functionality of **lists** with lazy content loading.<br/>

```bash
An example to read file contents using generator

def read_fle(filename):
	with open(filename, "r") as f:
		yield from f

The yield statement allows the function to read the contents of the file line-by-line

The above function can be used like below
contents = read_file('file1.txt')

>> next(contents)
Retrieves a line from the file

Can also use the for loop to iterate through contents
for cont in contents:
	print(cont)
```
<br/>

### Yield vs Return
**return**: When 'return' is encountered in a function, the execution stops there, states are cleared and control goes back to caller<br/>
**yield**: When 'yield' is encountered inside a function, the functionality is paused. When the function is called next time, the execution start from where it stopped previously rather than from the beginning.<br/>

### Lazy Loading
By having the lazy loading facility, Generators allow reading huge files without impact on the system resources. Even though the file size is 10GB, we still read a single line from the file thus allowing the functionality to work on machines with normal computing power.<br/>
Generators functions are frequently used in dataloaders.<br/>

### Item Exhaustion
Like the Iterators, Generators also gets exhausted after reaching the end of the elements.<br/>
By adding iterables, Generators allow to have infinite execution of the function without exhaustion.<br/>

### Project Work
#### Goal 1
Create a lazy iterator that will return a named tuple of the data in each row. The data types should be appropriate - i.e. if the column is a date, you should be storing dates in the named tuple, if the field is an integer, then it should be stored as an integer, etc. <br/>

#### Goal 2
Calculate the number of violations by car make.<br/>

#### Note:
Try to use lazy evaluation as much as possible - it may not always be possible though! That's OK, as long as it's kept to a minimum.<br/>

The assignment is available as Colab Notebook: https://colab.research.google.com/drive/1LCrybfdhIy7f3Sy1UEVNhPnLt1r-EU9Y?usp=sharing <br/>

### Code Overview
The highlevel steps involved in the code is given below for easier understanding <br/>
The file used is: nyc_parking_tickets_extract-1.csv (available in the repo for downloading). The file contains the list of parking violations information in NYC.<br/>
1. Read the contents of the file -> As Generator Function<br/>
2. Create NamedTuple to better structure the contents<br/>
3. Maintain the datatype of each field for computation purposes<br/>
4. Compute the number of violations by car make

### Class Overview
#### ParkingTickets
ParkingTickets is a class to lazily read the contents of the file<br/>
The class contains a static method with 'yield', which allows to iterate through each line only when required

#### Tickets
Tickets is a class to lazily fetch each ticket information, convert to a namedtuple <br/>
It also has a method to compute the violations made by each car make<br/>
