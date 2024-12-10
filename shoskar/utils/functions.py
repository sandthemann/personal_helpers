import inspect

def filter_kwargs(func, kwarg_dict):
    """filter kwargs to only a set that matches the function they will be passed to"""
    sign = inspect.signature(func).parameters.values()
    sign = set([val.name for val in sign])

    common_args = sign.intersection(kwarg_dict.keys())
    filtered_dict = {key: kwarg_dict[key] for key in common_args}

    return filtered_dict

def assertion(rule, error, error_string):
      """
        asserts that different inputs are strings
    
        args:
          -rule: formula that evaluates to True/False (bool)
          -error: Error Type to return (ex. KeyError, ValueError)
          -error_string: string to return if there is an error
        output:
           None
      """
      if type(rule) != bool:
        raise ValueError(f'the rule should evaluate to a boolean, it is currently evaluating to {type(rule)}')
      if type(error_string) != str:
        raise ValueError(f'error_string should be a string, you provided a {type(error_string)}')
      if rule:
        pass
      else:
        raise error(error_string)
      
def assert_string(self, string_dict):
    """
    asserts that different inputs are strings

    args:
        -string_dict: string for names and variable names in a dictionary format, will check that each variable is a string (dict)
    output:
        None
    """
    assertion(isinstance(string_dict, dict), TypeError, f'string_dict must be a dict, you provided {type(string_dict)}')
    for k,v in string_dict.items():
        if not isinstance(v, str) and v is not None:
            raise TypeError(f"{k} should be a string, and you provided {type(v)}")