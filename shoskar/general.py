import string
import random
import itertools
from datetime import datetime, timedelta
# from functools import partial
# import pandas as pd

def is_valid_date(date_string):
    try:
        datetime.strptime(date_string, '%Y-%m-%d')
        return True
    except:
        return False

def generate_random_string(length = 10):
    return ''.join(random.choices(string.ascii_lowercase, k=length))
    
def find_consecutive_date_groups(dates):
    # Convert string dates to datetime objects
    dates = sorted([datetime.strptime(date, "%Y-%m-%d") for date in dates])
    
    # Group dates by consecutive days
    groups = []
    for k, g in itertools.groupby(enumerate(dates), lambda x: x[0] - (x[1] - dates[0]).days):
        group = list(map(lambda x: x[1], g))
        groups.append(group)
    
    return groups

def find_next_date(dates):
    return max(dates) + timedelta(days=1)

def find_previous_date(dates):
    return min(dates) + timedelta(days=-1)

def date_to_string(date):
    return date.strftime('%Y-%m-%d')

def min_max_values(list):
    min_value = min(list)
    max_value = max(list)
    return min_value, max_value

def min_max_equal(list):
    min_value, max_value = min_max_values(list)
    return min_value == max_value

# def alteryx_join(df1, df2, join_columns):
#   left_only = df1.join(df2, join_columns, 'left_anti')
#   inner = df1.join(df2, join_columns, 'left_anti')
#   right_only = df2.join(df1, join_columns, 'left_anti').select(left_only.columns)
#   return left_only, inner, right_only

