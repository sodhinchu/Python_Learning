import pytest
import inspect
import os
import re
import scopes_and_closures

README_CONTENT_CHECK_FOR = [
    'inner',
    'closure',
    'free',
    'variable',
    'fibonacci',
    'global',
    'counter',
    'docstring',
    'dictionary'
]

def test_readme_exists():
    assert os.path.isfile("README.md"), "README.md file missing!"

def test_readme_contents():
    readme = open("README.md", "r")
    readme_words = readme.read().split()
    readme.close()
    assert len(readme_words) >= 500, "Make your README.md file interesting! Add atleast 500 words"

def test_readme_proper_description():
    READMELOOKSGOOD = True
    f = open("README.md", "r")
    content = f.read()
    f.close()
    for c in README_CONTENT_CHECK_FOR:
        if c not in content:
            READMELOOKSGOOD = False
            pass
    assert READMELOOKSGOOD == True, "You have not described all the functions/class well in your README.md file"

def test_readme_file_for_formatting():
    f = open("README.md", "r")
    content = f.read()
    f.close()
    assert content.count("#") >= 10

def test_indentations():
    ''' Returns pass if used four spaces for each level of syntactically \
    significant indenting.'''
    lines = inspect.getsource(scopes_and_closures)
    spaces = re.findall('\n +.', lines)
    for space in spaces:
        assert len(space) % 4 == 2, "Your script contains misplaced indentations"
        assert len(re.sub(r'[^ ]', '', space)) % 4 == 0, "Your code indentation does not follow PEP8 guidelines" 

def test_function_name_had_cap_letter():
    functions = inspect.getmembers(scopes_and_closures, inspect.isfunction)
    for function in functions:
        assert len(re.findall('([A-Z])', function[0])) == 0, "You have used Capital letter(s) in your function names"


def test_function_docstringlen():
    def f1():
        '''
        This function is testing what is a docstring, how to get its length and whether it is exceeding 50
        characters or not. Lets test and identify
        '''
        pass

    def f2():
        '''
        This is a function
        '''
        pass

    def f3():
        pass

    def f4():
        #There is no docstring but the comments are there
        #Adding multiple comments
        #Count is more than 50 characters
        #Still this function should be treated as without docstring
        pass

    #Test-1: Should return True if the function has docstring > 50 characters
    doclensanity = scopes_and_closures.checkdoclen()
    assert doclensanity(f1) == True, "Function does not have enough documentation!" 

    #Test-2: Raise Value Error if the function has docstring < 50 characters but > 0
    with pytest.raises(ValueError):
        doclensanity(f2)
    #Test-3: Raise Value Error if the function has no docstring (no docstrig, no comments)
    with pytest.raises(ValueError):
        doclensanity(f3)
    #Test-4: Raise Value Error if the function has no docstring (but contains comments)
    with pytest.raises(ValueError):
        doclensanity(f4)

    #Test-5: Checking if the scopes_and_closures functions have enough documentation or not
    assert doclensanity(scopes_and_closures.checkdoclen) == True, "Function does not have enough documentation!" 
    assert doclensanity(scopes_and_closures.fibgen) == True, "Function does not have enough documentation!" 
    assert doclensanity(scopes_and_closures.globalcounter) == True, "Function does not have enough documentation!" 
    assert doclensanity(scopes_and_closures.funccounter) == True, "Function does not have enough documentation!" 

def test_fibonacci_number():
    fibonacci = scopes_and_closures.fibgen()
    #Test-1: Checking the starting value is '2' or not
    assert fibonacci() != 1, "Fibonacci number is not matched - This should be 2, but not 1!" 
    #Test-2: Checking whether the series is continuing or not: The new value should be '3'
    assert fibonacci() == 3, "Fibonacci number is not matched!" 

    #Test-3: Run in the loop for next 5 numbers and verify if the 6th number is matching or not
    #Above tests generated the series: 2, 3 and the following tests continue from 5 8 13 21 34
    for _ in range(5):
        fibonacci()
    #Now the number should be 55
    assert fibonacci() == 55, "Fibonacci number is not matched!" 


def add(a, b):
    return a+b

def mul(a, b):
    return a*b

def div(a, b):
    if b != 0:
        return a/b
    else:
        raise ValueError('Division by 0')

def test_global_dict_counts():
    #Test-1: Checking the number of calls to add()
    add_func = scopes_and_closures.globalcounter(add)
    add_counts = 3
    for index in range(add_counts):
        add_func(index, index+1)
    assert scopes_and_closures.countfunccalls['add'] == add_counts, 'Add Function Calls Count not Matched!'
    #Test-2: Checking the count is incremented even if the function is called with same arguments as previous
    add_func(index, index+1)
    assert scopes_and_closures.countfunccalls['add'] == (add_counts+1), 'Add Function Calls Count not Matched!'

    #Test-3: Checking the count is not incremented without function call
    assert 'mul' not in scopes_and_closures.countfunccalls, 'Mul Function Count incremented without a single call!'
    #Test-4: Checking if the count is incremented by 1 or uses previous calls of 'add'
    mul_func = scopes_and_closures.globalcounter(mul)
    mul_func(1, 2)
    assert scopes_and_closures.countfunccalls['mul'] == 1, 'Mul Function Calls Count not Matched!'
    #Test-5: Re-Checking if the count is incremented by calling function, also retained the previous calls
    mul_counts = 5
    for index in range(mul_counts):
        mul_func(index, index+1)
    assert 'add' in scopes_and_closures.countfunccalls, 'Add Function missing in the dictionary!'
    assert scopes_and_closures.countfunccalls['add'] == (add_counts+1), 'Add Function Calls Count not Matched!'
    assert scopes_and_closures.countfunccalls['mul'] == (mul_counts+1), 'Mul Function Calls Count not Matched!'

    #Test-6: Checking whether the count is incremented or not in valueerror scenario
    div_func = scopes_and_closures.globalcounter(div)
    with pytest.raises(ValueError):
        div_func(1, 0)
        assert scopes_and_closures.countfunccalls['div'] == 1, 'Div Function Calls Count not Matched!'
    #Test-7: Checking whether the count is incremented from previous count or not
    div_counts = 7
    for index in range(div_counts):
        div_func(index, index+1)
    assert scopes_and_closures.countfunccalls['div'] != div_counts, 'Div Function Calls Count Should not be Matched!'


def test_ind_dict_counts():
    #Test-1: Checking the number of calls to add()
    add_dict = dict()
    add_func = scopes_and_closures.funccounter(add, add_dict)
    add_counts = 3
    for index in range(add_counts):
        add_func(index, index+1)
    assert add_dict['add'] == add_counts, 'Add Function Calls Count not Matched!'
    #Test-2: Checking the count is incremented even if the function is called with same arguments as previous
    add_func(index, index+1)
    assert add_dict['add'] == (add_counts+1), 'Add Function Calls Count not Matched!'

    #Test-3: Checking the count is not incremented without function call
    mul_dict = dict()
    assert 'mul' not in mul_dict, 'Mul Function Count incremented without a single call!'
    #Test-4: Checking if the count is incremented by 1 or uses previous calls of 'add'
    mul_func = scopes_and_closures.funccounter(mul, mul_dict)
    mul_func(1, 2)
    assert mul_dict['mul'] == 1, 'Mul Function Calls Count not Matched!'
    #Test-5: Re-Checking if the count is incremented by calling function
    mul_counts = 5
    for index in range(mul_counts):
        mul_func(index, index+1)
    assert mul_dict['mul'] == (mul_counts+1), 'Mul Function Calls Count not Matched!'

    #Test-6: Checking whether the count is incremented or not in valueerror scenario|
    div_dict = dict()
    div_func = scopes_and_closures.funccounter(div, div_dict)
    with pytest.raises(ValueError):
        div_func(1, 0)
        assert div_dict['div'] == 1, 'Div Function Calls Count not Matched!'
    #Test-7: Checking whether the count is incremented from previous count or not
    div_counts = 7
    for index in range(div_counts):
        div_func(index, index+1)
    assert div_dict['div'] != div_counts, 'Div Function Calls Should not be Matched!'