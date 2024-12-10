import os
import glob
from string import punctuation as str_punctuation
from functools import partial
import datetime
import pandas as pd

def find_xls_files(directory, check_sub_dirs = 0):
    """searches file directory and optionally subdirectores for xls* files"""
    if check_sub_dirs == 1:
        pattern = os.path.join(directory, '**', '*.xls*')
        xls_files = glob.glob(pattern, recursive=True)
    else:
        pattern = os.path.join(directory, '*.xls*')
        xls_files = glob.glob(pattern)

    return xls_files


def split_file_path(file_path):
    # Split the file name and directory path
    file_name = os.path.basename(file_path)  # Get the file name
    file_dir = os.path.dirname(file_path)    # Get the directory path
    return file_name, file_dir


def normalize_string(normalize_str, punc = str_punctuation, case = 'lower', strip = True):
    """allows for the normalization of strings. str_punctuation is all punctuation."""
    if punc is not None:
        punc_table = str.maketrans('', '', punc)
        normalize_str = normalize_str.translate(punc_table)

    if case is not None:
        normalize_str = getattr(str, case)(normalize_str)
        
    if strip:
        normalize_str = normalize_str.strip()

    return normalize_str

#feature factory for above function
#sheet names allow almost all punctuation except for []*/\?:
normalize_sheet_name = partial(normalize_string, punc = '[]*/\?:')

normalize_column_names = partial(normalize_string, case = None, punc = None)

strip_string = partial(normalize_string, punc = None, case = None)

change_case_and_trim = partial(normalize_string, punc = None)


def convert_date(target_date):
    """date conversion for excel 1900 based dates, will not work with 1904 based dates."""
    #ensures the target value in question is not already a datetime type object
    if type(target_date) in (pd.Timestamp, datetime.datetime, datetime.datetime.date):
        return pd.to_datetime(target_date)
    
    #verifies the target is actually an int or float type
    if not isinstance(target_date, int) and not isinstance(target_date, float):
        return None

    #math
    if int(target_date) == 0:
        return datetime.datetime(1900, 1, 1, 0, 0, 0) + datetime.timedelta(seconds=round(target_date * 24 * 60 * 60))
    elif int(target_date) >= 61:
        # According to Lotus 1-2-3, Feb 29th 1900 is a real thing, therefore we have to remove one day after that date
        return datetime.datetime(1899, 12, 31, 0, 0, 0) + datetime.timedelta(days=int(target_date) - 1, seconds=round((target_date % 1) * 24 * 60 * 60))
    else:
        # Feb 29th 1900 will show up as Mar 1st 1900 because Python won't handle that date
        return datetime.datetime(1899, 12, 31, 0, 0, 0) + datetime.timedelta(days=int(target_date), seconds=round((target_date % 1) * 24 * 60 * 60))


