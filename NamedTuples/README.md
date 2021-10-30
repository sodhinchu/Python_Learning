# NamedTuples
namedtuple() is a class inside collections() module that helps to write the code more Pythonic way (to handle tuples) <br/>
namedtuple() assigns meaning to each position in tuple and offers more readable coding <br/>

The following shows how a namedtuple can be created <br/>
```bash
Example 1:
Student = namedtuple('Student', 'name course roll_number')
The RHS statement creates a namedtuple called 'Student' with the fields: name, class, roll_number

Using the above 'Student' multiple students details can be constructed like below
st1 = Student('rohan', 'epai3', 101)
st2 = Student('shravan', 'epai3', 102)
st3 = Student('zoheb', 'epai3', 103)

The fields can be accessed as
st1.name -> rohan
st1.roll_number -> 101
st2.class -> epai3
```
The following showcases the basic usage of namedtuple: <br/>
1. Instantiate with positional/keyword arguments <br/>
```bash
Student = namedtuple('Student', 'name course roll_number')
st1 = Student(name='rohan', course='epai3', roll_number=101)
st2 = Student('shravan', 'epai3', roll_number=101)
```
2. Indexable (like other iterables(list/tuples etc)) <br/>
```bash
>> st1[0]
rohan
>> st1[0] + ' ' + st2[0]
rohan shravan
```
3. Unpack (like a normal tuple) <br/>
```bash
>> student_name, student_course, student_roll_number = st1
>> student_name, student_course, student_roll_number
rohan, epai3, 101
```
4. Access the fields by name <br/>
```bash
>> st1.name + ' ' + st2.name
rohan shravan
```
5. Readable with name = value style <br/>
```bash
>> st1
Student(name='rohan', course='epai3', roll_number=101)
```

The operartors that can be used with namedtuple are: <br/>
1. _fields: Lists out the various attributes/fields of the namedtuple <br/>
In the above code snippet(Example1), st3._fields returns name, class, roll_number <br/>

2. _source: Lists out the source code for the namedtuple

3. _replace: To replace the values of fields in a namedtuple <br/>
```bash
>> st1 = Student(name='rohan', course='epai3', roll_number=101)
>> st1._replace(name='zoheb')
Student(name='zoheb', course='epai3', roll_number=101)
```

4. _asdict: Converts the named tuple to dictionary <br/>
```bash
st1 = Student('rohan', 'epai3', 101)
st1_dict = st1._asdict

type(st1) -> __main__.Student
type(st1_dict) -> collections.OrderedDict
```

Advantages of namedtuples over other dictionaries <br/>
1. Wherever tuples are used and need better readable/documented code, go for namedtuples <br/>
2. Useful for handling large csv/databases where indexing becomes messy and beneficial to have named attributes
3. Lighter weight than dictionaries, yet maintains order like dictionary <br/>

Other things to consider while using namedtuples <br/>
1. Like tuples, namedtuples are also immutable, meaning once created, new fields cannot be added
```bash
Student = namedtuple('Student', 'name course roll_number')
st1 = Student('rohan', 'epai3', 101)
>> st1.marks = 90
Unlike dictionary, new attributes cannot be created and assigned dynamically
```
## Project Work
1. Use the Faker (Links to an external site.)library to get 10000 random profiles. Using namedtuple, calculate the largest blood type, mean-current_location, oldest_person_age, and average age (add proper doc-strings). - 250 (including 5 test cases) <br/>
2. Do the same thing above using a dictionary. Prove that namedtuple is faster. - 250 (including 5 test cases) <br/>
3. Create fake data (you can use Faker for company names) for imaginary stock exchange for top 100 companies (name, symbol, open, high, close). Assign a random weight to all the companies. Calculate and show what value the stock market started at, what was the highest value during the day, and where did it end. Make sure your open, high, close are not totally random. You can only use namedtuple. - 500  (including 10 test cases) <br/>
