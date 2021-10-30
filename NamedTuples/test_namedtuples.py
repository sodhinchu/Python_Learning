import session9
from session9 import *
import datetime
import pytest
from io import StringIO 
import sys
import time
import inspect
import os
import re
from decimal import Decimal

README_CONTENT_CHECK_FOR = [
    "namedtuple",
    'tuple',
    "dictionary",
    "compare",
    'time',
    "faster",
    "slower",
    'faker',
    'fake',
    'profile',
    'profiles',
    'blood group',
    'current location',
    'current',
    'location',
    'age',
    'oldest',
    'largest',
    'average',
    'mean',
    "stock",
    "stocks",
    "exchange",
    "name",
    'symbol',
    "open",
    "high",
    'peak',
    "close",
    'gain',
    "loss",
    "market",
    "momentum"
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
    f = open("README.md", "r", encoding="utf-8")
    content = f.read()
    f.close()
    for c in README_CONTENT_CHECK_FOR:
        if c not in content:
            READMELOOKSGOOD = False
            pass
    assert READMELOOKSGOOD == True, "You have not described all the functions/class well in your README.md file"

def test_readme_file_for_formatting():
    f = open("README.md", "r", encoding="utf-8")
    content = f.read()
    f.close()
    assert content.count("#") >= 10

def test_indentations():
    ''' Returns pass if used four spaces for each level of syntactically \
    significant indenting.'''
    lines = inspect.getsource(session9)
    spaces = re.findall('\n +.', lines)
    for space in spaces:
        assert len(space) % 4 == 2, "Your script contains misplaced indentations"
        assert len(re.sub(r'[^ ]', '', space)) % 4 == 0, "Your code indentation does not follow PEP8 guidelines"

def test_function_name_had_cap_letter():
    functions = inspect.getmembers(session9, inspect.isfunction)
    for function in functions:
        assert len(re.findall('([A-Z])', function[0])) == 0, "You have used Capital letter(s) in your function names"

def test_profile():
    num_profiles = 10
    profiles = generate_profiles(num_profiles)
    #T1: Validation checks on profile data
    assert len(profiles) == num_profiles, 'Mismatch in length of profiles'
    assert('g' not in [profile.blood_group for profile in profiles]), 'Hmm! \'g\' seems to be a rare blood-group, never heard of it!'
    assert(0 not in [profile.latitude for profile in profiles]), 'No zer-coordinates for location!'
    assert(0 not in [profile.longitude for profile in profiles]), 'No zer-coordinates for location!'

    #T2: Validating namedtuples properties
    assert ('birthdate' in profiles[0]._fields), 'Failure in checking data with fields'

    Profile = namedtuple('Profile', 'blood_group latitude longitude birthdate age')
    p1 = Profile('AB+', 52.958961, 143.143712, datetime.date(1944, 8, 30), 42360)
    p2 = Profile('A-', -20.228286, -142.416727, datetime.date(1943, 8, 15), 41295)
    p = [p1, p2]
    p_return = generate_profiles(num_profiles=2, profiles=p)
    #T3: Comparing two namedtuples
    assert(p_return == p), 'The namedtuples should match'
    #T4: Checking for immutability
    with pytest.raises(TypeError) as execinfo:
        p_return[0]['gender'] = 'M'
    #T5: Checking replace() functionality
    p3 = Profile('AB+', 73.100442, 171.844720, datetime.date(1944, 8, 30), 42360)
    p1 = p1._replace(latitude=73.100442, longitude=171.844720)
    assert(p1 == p3), 'Replace did not update field values as expected'

    #T6: Compare results for namedtuples vs dictionaries
    num_profiles = 10000
    profiles = generate_profiles(num_profiles)
    profiles_dict = generate_profiles_dict(num_profiles, profiles)

    result_bt_nt = calc_time_nt_largest_blood_group(profiles)
    result_bt_dict = calc_time_dict_largest_blood_group(profiles_dict)
    #Comparing results for largest blood type
    assert(result_bt_nt == result_bt_dict), 'Largest Blood Type results are not matching'

    result_loc_nt = calc_time_nt_mean_current_location(profiles)
    result_loc_dict = calc_time_dict_mean_current_location(profiles_dict)
    #Comparing results for mean current location
    assert(result_loc_nt == result_loc_dict), 'Mean Current Location results are not matching'

    oldest_age_nt, average_age_nt = calc_time_nt_oldest_average_age(profiles)
    oldest_age_dict, average_age_dict = calc_time_dict_oldest_average_age(profiles_dict)
    assert(oldest_age_nt == oldest_age_dict), 'Oldest Age results are not matching'
    assert(average_age_nt == average_age_dict), 'Average Age results are not matching'

def test_compare_nt_dict_perf():
    profiles = generate_profiles(num_profiles = 1)

    #T1: Accessing Fields
    time_nt, _ = nt_field_access(profiles[0], profiles[0].blood_group)
    time_dict, _ = dict_field_access(dict(profiles[0]._asdict()), profiles[0].blood_group)
    assert(time_nt < time_dict), 'FieldAccess: Dictionaires are faster than NamedTuples!'

    #T2: Memory Usage
    _, nt_size = nt_size_compare(profiles[0])
    _, dict_size = dict_size_compare(dict(profiles[0]._asdict()))
    assert(nt_size < dict_size), 'Memory Usage: Dictionaires occupy less memory than NamedTuples!'

    #T3: Comparing two instances
    time_nt = nt_instance_compare(profiles[0], profiles[0])
    time_dict = dict_instance_compare(dict(profiles[0]._asdict()), dict(profiles[0]._asdict()))
    assert(time_nt < time_dict), 'Instance Compare: Dictionaires are faster than NamedTuples!'

    #T4: Unpacking values
    time_nt = nt_unpacking(profiles[0])
    time_dict = dict_unpacking(dict(profiles[0]._asdict()))
    assert(time_nt < time_dict), 'Unpack Values: Dictionaires are faster than NamedTuples!'

    #T5: create new instance
    Profile = namedtuple('Profile', 'blood_group latitude longitude birthdate age')
    new_values = ['AB+', 123.45, 67.8, date(1979, 2, 22), 32456]
    time_nt, _ = nt_create_new_instance(Profile, new_values)
    time_dict, _ = dict_create_new_instance(new_values)
    assert(time_nt < time_dict), 'Create New Instance: Dictionaires are faster than NamedTuples!'

def test_stock_exchange():
    stocks, weights = session9.create_stock_exchange(100)
    #T1: Validation checks
    assert len(stocks) == 100, 'Supposed to generate 100 company stocks'

    #T2: NamedTuple Immutability check: Cannot create and assign new fields dynamically
    with pytest.raises(TypeError) as execinfo:
        stocks[0]['ipo'] = True

    *_, open, high, close = list(zip(*stocks))
    for index in range(len(stocks)):
        #T3: Close should always be <= high value for the day
        assert(close[index] <= high[index])
        #T4: High should always be >= open value for the day
        assert(high[index] >= open[index])
        #T5: Open should always be > 0
        assert(open[index] > 0)


    def generate_random_stocks(for_gain = True):
        '''
        Dummy function to create 3 stocks with their open, high, close and their weights of the stock exchange
        for_gain = True
            The open, high, close -> Chosen such a way that, the market is upwards
        for_gain = False
            The open, high, close -> Chosen such a way that, the market is downwards
        '''
        Stock = namedtuple('Stock', 'name symbol open high close')
        if for_gain:
            tsai = Stock('TSAI', 'TSA', 1400, 1560, 1500)
            skunkworks = Stock('SKUNKWORKS', 'SKW', 2000, 2300, 2050)
            inkers = Stock('INKERS', 'INK', 1675, 1987, 1900)
        else:
            tsai = Stock('TSAI', 'TSA', 1400, 1400, 1200)
            skunkworks = Stock('SKUNKWORKS', 'SKW', 2000, 2000, 1850)
            inkers = Stock('INKERS', 'INK', 1675, 1675, 1500)

        weights = [0.45, 0.35, 0.2]
        return [tsai, skunkworks, inkers], weights

    stocks, weights = generate_random_stocks(for_gain=True)
    stocks_new, weights_new = session9.create_stock_exchange(3, stocks, weights)
    #T6 - Validating if values can be set from outside [Also NamedTuples can be compared directly]
    assert stocks_new == stocks, 'Stock Values weren\'t supposed to be modified'
    assert weights_new == weights, 'Weights Values weren\'t supposed to be modified'

    #T7: Market Gain Check
    assert 'gain' in session9.get_market_momentum(stocks_new, weights_new), 'Market should be gaining!'

    stocks, weights = generate_random_stocks(for_gain=False)
    stocks_new, weights_new = session9.create_stock_exchange(3, stocks, weights)
    #T8: Market Loss Check
    assert 'lost' in session9.get_market_momentum(stocks_new, weights_new), 'Market is supposed to be in loss!'



