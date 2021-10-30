import sys
from collections import namedtuple, Counter
from datetime import date
from random import choice, randint, uniform
from faker import Faker

def getfaker_obj():
    '''
    Faker is a python library to generate fake data
    Function which returns the faker object
    Seed helps to generate the same data in multiple runs of the function
    '''
    Faker.seed(47)
    fake = Faker()
    return fake

def getfaker_profile(fakerobj):
    '''
    Function to generate fake profile data
    Profile contains information like name, gender, job, ssn, current location, birthdate etc.
    Since we are interested only in certain fields, create a namedtuple to hold that information
    Interested fields for inspection are: blood_group, current_location age
    '''
    profile = fakerobj.profile()

    # Faker profile contains birthdate and from which age is calculated
    today = date.today()
    age = (today - profile['birthdate']).days

    Profile = namedtuple('Profile', 'blood_group latitude longitude birthdate age')
    # Returning the relevant profile information in a named tuple
    return Profile(profile['blood_group'], float(profile['current_location'][0]), \
                    float(profile['current_location'][1]), profile['birthdate'], age)

def generate_profiles(num_profiles = 1, profiles = None):
    '''
    Function to generate the fake profiles
    num_profiles denote the number of profiles requried to generate
    Default value is '1' and can be changed by the caller
    '''
    if profiles is not None:
        profiles_list = profiles
    else:
        profiles_list = []
        fake = getfaker_obj()
        for _ in range(num_profiles):
            # Update the list with each profile generated
            profiles_list.append(getfaker_profile(fake))
    return profiles_list

def getfaker_profile_dict(fakerobj):
    '''
    Function to generate fake profile data
    Profile contains information like name, gender, job, ssn, current location, birthdate etc.
    Interested fields for inspection are: blood_group, current_location age
    '''
    profile = fakerobj.profile()

    today = date.today()
    age = (today - profile['birthdate']).days

    profile_dict = dict.fromkeys(['blood_group', 'latitude', 'longitude' 'birthdate', 'age'], 0)

    profile_dict['blood_group'] = profile['blood_group']
    profile_dict['latitude'] = profile['current_location'][0]
    profile_dict['longitude'] = profile['current_location'][1]
    profile_dict['birthdate'] = profile['birthdate']
    profile_dict['age'] = age
    return profile_dict

def generate_profiles_dict(num_profiles = 1, profiles = None):
    '''
    Function to generate the fake profiles
    num_profiles denote the number of profiles requried to generate
    Default value is '1' and can be changed by the caller

    if profiles is sent by the caller the same information is used to populate the dictionary
    else new profiles will be created in dict fashion
    '''
    profiles_dict = {}
    if profiles is not None:
        for index, profile in enumerate(profiles):
            profiles_dict[index] = dict(profile._asdict())
    else:
        fake = getfaker_obj()
        for index in range(num_profiles):
            # Update the list with each profile generated
            profiles_dict[index] = getfaker_profile(fake)
    return profiles_dict

def calc_time_nt_largest_blood_group(profiles):
    '''
    Calculates the largest blood group from the list of profiles
    Extracts the blood_group to a list and use Counter to find the largest available blood group
    '''
    blood_group_list = []  

    for profile in profiles:
        # profile is a namedtuple and fields can be accessed using . (dot) operator
        blood_group_list.append(profile.blood_group)

    large_blood_group = Counter(blood_group_list).most_common(1)
    return large_blood_group

def calc_time_dict_largest_blood_group(profiles):
    '''
    Calculates the largest blood group from the list of profiles
    Extracts the blood_group to a list and use Counter to find the largest available blood group
    '''
    blood_group_list = []  
    #profiles is a dictionary and iterated among its values
    for profile in profiles.values():
        blood_group_list.append(profile['blood_group'])

    large_blood_group = Counter(blood_group_list).most_common(1)
    return large_blood_group

def calc_time_nt_mean_current_location(profiles):
    '''
    Calculates the mean current location from the list of profiles
    Extracts the lattitude and longitude to a list and computes average
    '''
    lat_list = []
    long_list = []

    for profile in profiles:
        lat_list.append(float(profile.latitude))
        long_list.append(float(profile.longitude))

    mean_location = [sum(lat_list)/len(profiles), sum(long_list)/len(profiles)]
    return mean_location

def calc_time_dict_mean_current_location(profiles):
    '''
    Calculates the mean current location from the list of profiles
    Extracts the lattitude and longitude to a list and computes average
    '''
    lat_list = []
    long_list = []

    for profile in profiles.values():
        lat_list.append(float(profile['latitude']))
        long_list.append(float(profile['longitude']))

    mean_location = [sum(lat_list)/len(profiles), sum(long_list)/len(profiles)]
    return mean_location


def calc_time_nt_oldest_average_age(profiles):
    '''
    Calculates the oldest age and average age from the list of profiles
    Extracts the age information to a list and computes maximum value and average
    '''
    age_list = []

    for profile in profiles:
        age_list.append(profile.age)

    oldest_age = max(age_list)
    average_age = (sum(age_list)/len(profiles))
    return oldest_age, average_age

def calc_time_dict_oldest_average_age(profiles):
    '''
    Calculates the oldest age and average age from the list of profiles
    Extracts the age information to a list and computes maximum value and average
    '''
    age_list = []

    for profile in profiles.values():
        age_list.append(profile['age'])

    oldest_age = max(age_list)
    average_age = (sum(age_list)/len(profiles))
    return oldest_age, average_age

def timed(repeats=1):
    '''
    Decorator factory to compute the average running time of a function
    repeats is an input argument which indicates how many times the function will be running for average time computation
    default value for repeats = 1 and can be changed by the caller
    '''
    def timer_decorator(fn):
        from time import perf_counter
        from functools import wraps
        @wraps(fn)
        def inner(*args, **kwargs):
            # Call the function for repeats times and compute the average running time for each call
            total_elapsed = 0
            for _ in range(repeats):
                start = perf_counter()
                result = fn(*args, **kwargs)
                end = perf_counter()
                total_elapsed += (end-start)
            avg_time = (total_elapsed/repeats)* int(1e9) #Nano Seconds
            print(f'{fn.__name__}() average running_time: {avg_time:.3f}msec for {repeats} repetitions')
            return round(avg_time, 3), result
        return inner
    return timer_decorator

@timed(1_000_000)
def nt_field_access(profile, check_value):
    '''
    Function to access the fields of a namedtuple
    This is to check how much time it takes to access fields in namedtuple object
    '''
    'latitude' in profile._fields
    'blood_group' in profile._fields
    'random_field' in profile._fields
    check_value in profile
    profile.age

@timed(1_000_000)
def dict_field_access(profile_dict, check_value):
    '''
    Function to access the fields of a dictionary
    This is to check how much time it takes to access fields in dictionary object
    '''
    'latitude' in profile_dict
    'blood_group' in profile_dict
    'random_key' in profile_dict
    check_value in profile_dict.values()
    profile_dict['age']

@timed(1_000_000)
def nt_size_compare(profile):
    '''
    Function to retrieve the memory occupied by namedtuple
    '''
    return sys.getsizeof(profile)

@timed(1_000_000)
def dict_size_compare(profile_dict):
    '''
    Function to retrieve the memory occupied by namedtuple
    '''
    return sys.getsizeof(profile_dict)

@timed(1_000_000)
def nt_instance_compare(profile1, profile2):
    '''
    Function to compare multiple objects of a namedtuple
    '''
    return profile1 == profile2

@timed(1_000_000)
def dict_instance_compare(profile_dict1, profile_dict2):
    '''
    Function to compare multiple objects of a namedtuple
    '''
    return profile_dict1 == profile_dict2

@timed(1_000_000)
def nt_unpacking(profile):
    '''
    Function to unpack the values from namedtuple
    '''
    blood_group, latitude, longitude, birthdate, age = profile
    return blood_group, latitude, longitude, birthdate, age

@timed(1_000_000)
def dict_unpacking(profile_dict):
    '''
    Function to unpack the values from dictionary
    '''
    blood_group, latitude, longitude, birthdate, age = profile_dict.values()
    return blood_group, latitude, longitude, birthdate, age

@timed(1_000_000)
def nt_create_new_instance(nt_class, new_values):
    '''
    Function to create new instance for the given named tuple
    '''
    profile_new = nt_class._make(new_values)
    return profile_new

@timed(1_000_000)
def dict_create_new_instance(new_values):
    '''
    Function to create new instance for the given dictionary
    '''
    profile_dict_new = dict.fromkeys(['blood_group', 'latitude', 'longitude' 'birthdate', 'age'], 0)
    profile_dict_new['blood_group'] = new_values[0]
    profile_dict_new['latitude'] = new_values[1]
    profile_dict_new['longitude'] = new_values[2]
    profile_dict_new['birthdate'] = new_values[3]
    profile_dict_new['age'] = new_values[4]
    return profile_dict_new

def calc_open_value(stocks, weights):
    '''
    Computes and returns the opening value of the stock exchange
    '''
    *_, open, high, close = list(zip(*stocks))
    open_values = []
    # Iterate through each stock, multiply the its opening and weightage
    # Sum of the above gives the market opening value
    for index, num in enumerate(open):
        open_values.append(num*weights[index])
    return sum(open_values)

def calc_high_value(stocks, weights):
    '''
    Computes and returns the highest value for the day of the stock exchange
    '''
    *_, open, high, close = list(zip(*stocks))
    high_values = []
    # Iterate through each stock, compute the difference between its highest and opening value
    # Multiply the difference with the weight of the stock
    # Sum of the above with the market_open_value of the day gives the market highest point
    for index in range(len(open)):
        diff = high[index]-open[index]
        high_values.append(diff*weights[index])
    open_values = calc_open_value(stocks, weights)
    return sum(high_values) + open_values

def calc_close_value(stocks, weights):
    '''
    Computes and returns the closing value of the stock exchange
    '''
    *_, open, high, close = list(zip(*stocks))
    close_values = []
    # Iterate through each stock, compute the difference between its closing and opening value
    # Multiply the difference with the weight of the stock
    # Sum of the above with the market_open_value of the day gives the market closure value
    for index in range(len(open)):
        diff = close[index]-open[index]
        close_values.append(diff*weights[index])
    open_values = calc_open_value(stocks, weights)
    return sum(close_values) + open_values


def get_market_momentum(stocks, weights):
    '''
    Function to track market momentum
    Given the current values of Stocks, the function computes whether market is going upwards or downwards
    Returns the gain/loss adjusted to 2 decimal points
    '''
    market_open = calc_open_value(stocks, weights)
    market_close = calc_close_value(stocks, weights)
    diff = (market_close - market_open)
    if(diff > 0):
        return f'Markets gained {diff:.2f} points'
    elif(diff == 0):
        return f'Markets are continuing study at {market_open:.2f} points'
    else:
        return f'Markets lost {diff:.2f} points'


def create_stock_exchange(num_stocks=1, stock_values=None, weight_values = None):
    '''
    Function to create stock exchange with the number of stocks requested
    Each stock contains name, symbol, open, high, close values for the trading day
    Random weights are assigned to each company and all the weights ensured to sum up to 1
    The function returns the stocks and the associated weights to the caller
    '''
    def get_stock_info(faker):
        '''
        Uses faker library to generate company names
        Symbol name is choosen as the first part of the company name(Split using spaces)
        Open:
            Indicates the open value of the stock for the given day
            Ranges from 1 to 1500
        High:
            Indicates the highest value the stock touched for the given day
            Ranges from (open to 2000) (or) equal to open
            These two sets of values are used randomly to simulate stock going upwards, downwards
        Close:
            Indicates the closing value of the stock for the given day
            Ranges from (1 to open) (or) equal to high
            These two sets of values are used randomly to simulate stock going upwards, downwards
        The function returns a namedtuple Stock with all the necessary values loaded
        '''
        Stock = namedtuple('Stock', 'name symbol open high close')
        name = faker.company()
        symbol = name.split()[0]
        open = randint(1, 1500)
        if(choice([0,1])):
            high = randint(open, 2000)
            close = high
        else:
            high = open
            close = randint(1, open)
        return Stock(name, symbol, open, high, close)

    def generate_stock_prices(num_stocks=1):
        '''
        This function generates number of stocks based on input argument (default value = 1)
        Each ticker is nothing a but a company stock and will be added to the list of stocks

        The function returns a list with each element is a namedtuple of type 'Stock'
        Check the function get_stock_info() to get more information on 'Stock' namedtuple
        '''
        stocks = []
        fake = Faker()
        Faker.seed(101)
        for _ in range(num_stocks):
            ticker = get_stock_info(fake)
            stocks.append(ticker)
        return stocks

    def generate_stock_weights(num_stocks=1):
        '''
        Function to generate (random) weightage to each listed company in the stock exchange
        Ensured that all the weights sum up to 1
        '''
        w1 = [uniform(0.01, 0.4) for _ in range(num_stocks)]
        weights = [(num/sum(w1)) for num in w1]
        return weights
    # If caller doesn't pass any pre-loaded information for stocks, generate them
    if stock_values is None:
        stocks = generate_stock_prices(num_stocks)
    else:
        # Setting with the values shared by the caller
        stocks = stock_values

    # If caller doesn't pass any pre-loaded information for weights, generate them
    if weight_values is None:
        weights = generate_stock_weights(num_stocks)
    else:
        # Setting with the values shared by the caller
        weights = weight_values
    return stocks, weights