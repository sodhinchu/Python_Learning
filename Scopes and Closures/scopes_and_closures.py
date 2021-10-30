def checkdoclen():
    '''
    This is a closure function to verify the documentation available for a given function
    The minlen is set as 50 characters and failing which the function throws
    valueerror depending on the length
    '''
    minlen = 50
    def inner(func):
        if(func.__doc__ != None):
            doclen = len(func.__doc__)
            if (doclen >= minlen):
                return True
            else:
                raise ValueError('Documentation is not upto the mark!')
        else:
            raise ValueError('No documentation available!!')
    return inner

def fibgen():
    '''
    This is a closure function to generate fibonacci numbers
    a, b : are the starting values of the fibonacci series.
    These can be changed by passing the starting values to fibgen() function
    a, b : also the free variables for the closure and can be found using func.__code__.co_freevar
    '''
    a = 1
    b = 1
    def inner():
        '''
        This is the inner function which generates the next fibonacci number
        Takes the current values (a, b) and generates the next number
        Since a, b values are modified inside the function, they are declared as non-local
        '''
        nonlocal a, b
        c = a+b
        a = b
        b = c
        return c
    return inner

#Global Dictionary to keep track of function calls
countfunccalls = dict()

def globalcounter(func):
    '''
    This is a closure function to keep track of the function calls
    It uses a global dictionary [countfunccalls] and uses a closure function to track the counter
    The function calls are shown as the <function name> <count>
    '''
    #Initial value for the counter
    count = 0
    def inner(*args, **kwargs):
        '''
        count is the free variable and accessed, modified inside the inner function
        count has initial value of zero and gets incremented with each function call
        Since the function scope is created newly, everytime a call is made for globalcounter()
        with a new function, the counter value starts at 0 or with the previous value
        '''
        nonlocal count
        #Counter value is incremented for each call
        count += 1
        countfunccalls[func.__name__] = count
        return func(*args, **kwargs)
    return inner

def funccounter(func, funcdict):
    '''
    This is a closure function to keep track of the function calls
    It uses the dictionary [funcdict] passed as argument to keep track of the
    counter with the inner function
    The function calls are shown as the <function name> <count>
    '''
    #Initial value for the counter
    count = 0
    def inner(*args, **kwargs):
        '''
        count is the free variable and accessed, modified inside the inner
        function
        count has initial value of zero and gets incremented with each
        function call
        Since the function scope is created newly, everytime a call is
        made for funccounter()
        with a new function, the counter value starts at 0 or with the
        previous value
        '''
        nonlocal count
        #Counter value is incremented for each call
        count += 1
        funcdict[func.__name__] = count
        return func(*args, **kwargs)
    return inner