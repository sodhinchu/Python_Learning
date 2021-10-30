# Scopes and Closures
This focuses on understanding the built-in, global, local, enclosing(nonlocal) spaces. Let's dive-in <br/><li/>
Built-in Scope: Also called as Python scope <br/>
The scope where the functions like print(), dict() enums like True, False fall in this space <br/>
These are available for all python files/modules/functions<li/>
Global Scope: Also called as module scope <br/>
The scope where the file resides and all its variables/functions fall in this spaces<br/><li/>
Local Scope: The scope of the function - All its inner functions, variables fall in this <br/><li/>
Enclosing Scope: Also called as nonlocal scope<br/>
The functions/variables mentioned in the outer function() of an inner function<br/><li/>
While parsing the code, python follows local scope -> enclosing space -> global space -> built-in scope <br/><li/>

The variables in the outer scope can be modifed via 'nonlocal' tag inside the inner function<br/>
Similarly the variables in the global scope can be modified via 'global' tag inside the function(s)<br/>

The below functions test the scope in various test scenarios. <br/>

## Functions Overview

### checkdoclen()
This is a closure function to verify the docstring of a query function <br/>
docstring: This is different from code comments, retained throughout the runtime and helps inspecting during runtime<br/>
Currently '50 characters' is set as the limitand it is a free variable inside the function.<br/>
The function can be further modified to take this minimum length as argument to be changed for each function<br/>

There are multiple tests to verify whether the function working as expected<br/>
Tested for both positive and negatvie scenarios<br/>
```bash
Positive: Function with a docstring = 50 characters
Expected Outcome: Returns True

Negative: 
i) Function with a docstring < 50 characters
ii) Function with no docstring but comments with length >= 50 characters
iii) Function with no docstring and no comments
Expected Outcome: Raises ValueError

Also used this function to ensure the functions in session7.py follow proper documentation or not
```

### fibgen()
This is a closure function to generate fibonacci numbers
Currently the starting values of the series are set as 1, 1 [free variables]
The function can be further modified to take the initial values of the series as arguments to change as (0, 1)
Tested for the following scenarios
```bash
Test 1: The first number output
Expected Outcome: Returns 2

Test 2: Checking if the series is continuing by examining next output
Expected Outcome: Returns 3

Test 3: Run a loop for 5 numbers and check whether the series is still continuing or not
If the series starting as 1 , 1, 2, 3
Next 5 numbers would be: 5, 8, 13, 21, 34
Expected Outcome: Returns 55
```

### globalcounter()
This is a closure function to keep track of the function calls
There is a counter which is a free variable (initialized as 0) in the globalcounter() local space
The function calls are tracked using a global dictionary which maintains the count against the function name
The idea is to check if the global dictionary gets updated for each function call with respective counts
but not contnuing with other function calls
```bash
Test 1: Call add func() for 'n' times and verify if the dictionary count is updated or not
Expected Outcome: dict['add'] = n

Test 2: Call add func() for one more time with previous arguments, to ensure functin counter still continue to update
Expected Outcome: dict['add'] = n+1

Test 3: Check if 'dict' contains any entry before calling the 'mul' function
Expected Outcome: 'mul' key should not be in the dict

Test 4: Call mul func() once to check if the count for this function starts at 1 or not
Expected Outcome: dict['mul'] = 1

Test 5: Call mul func() for 'n' times and verify now the dictionary contains both 'add' and 'mul' counts
Expected Outcome: 'add', 'mul' keys and with respective counts

Test 6: Call div() func to check for division by 0 error. In this case also, dictionary count should be updated
Expected Outcome: dict['div'] = 1

Test 7: Call div() func for 'n' times and verify if the dictionary count is updated from previously or not
Expected Outcome: dict['div'] = n+1
```

### funccounter()
This is a closure function to keep track of the function calls by passing relevant dictionaries to maintain the count<br/>
This function is exactly similar to above function globalcounter except that the dictionaries are passed
as argument rather than using a global dictionary<br/>
The test cases are also same as abobe function<br/>
