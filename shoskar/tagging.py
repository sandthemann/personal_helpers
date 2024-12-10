from typing import Callable, Dict, List, Any, Type
# import inspect
import sys

#before python 3.10, static methods were not considered a Callable
if sys.version_info < (3,10):
    sys.exit(f'Python < 3.10 is not supported, your version is {sys.version_info[0]}.{sys.version_info[1]}')

def tag(*tags):
    """
    Decorator function that adds tags to a function or method.
    
    Parameters:
    *tags: Variable number of tags to be associated with the function or method.
    
    Returns:
    Callable: Decorator function that adds the tags to the function or method.
    """
    def tags_decorator(func):
        func.tags = list(tags)
        return func
    return tags_decorator


def tagged_objects(obj: Dict[str, Callable]) -> List[Callable]:
    """
    Finds all tagged object associated with the provided dictionary.
    
    Parameters:
    obj: Dict[str, Callable]: Dictionary object to search for functions with tags. Ex. globals() or <YourClass>.__dict__.
    
    Returns:
    List[Callable]: List of functions/methods in the from the dictionary that have an attribute 'tags'.
    """
    
    v_objs = [func for name, func in obj.items() if callable(func)]
    v_funcs = [func.__func__ if '__func__' in dir(func) else func for func in v_objs]
    v_tagged = [obj for obj in v_funcs if 'tags' in dir(obj)]
    return v_tagged
        
def find_tags(obj: Dict[str, Callable]) -> Dict[str, List[str | int | bool]]:
    """
    Find all the tags associated with each method.
    
    Parameters:
    obj: Dict[str, Callable]: Dictionary object to search for tags. Ex. globals() or <YourClass>.__dict__.
    
    Returns:
    Dict[str, List[str | int | bool]]: Dictionary of methods and their associated tags.
    """

    v_tagged = tagged_objects(obj)
    v_tag_dict = {obj.__name__:obj.tags for obj in v_tagged}
    return v_tag_dict

def search_tag(obj: Dict[str, Callable], tag: str) -> Dict[str, Callable]:
    """
    Search for methods with a specific tag.

    Parameters:
    tag (str | int | bool): Tag to search for.

    Returns:
    List[Callable]: List of methods with the specified tag.
    """
    assert isinstance(tag, (str, int, bool)), ValueError(f'Tags can only be strings, ints, or bools. You provided {type(tag)}')
    
    v_tagged = tagged_objects(obj)
    v_evaluate_tag = lambda tag, obj: tag in [i for i in obj.tags if type(i) == type(tag)] 
    v_method_dict = {obj.__name__:obj for obj in v_tagged if v_evaluate_tag(tag, obj)}
    return v_method_dict
     
def search_tags(obj: Dict[str, Callable], tags: list | tuple | set) -> Dict[str, Callable]:
    """
    Search for methods with multiple tags.

    Parameters:
    tags (list | tuple | set): Tags to search for.

    Returns:
    Dict[str, Callable]: Dictionary of methods with the specified tags.
    """
    assert isinstance(tags, (list, tuple, set)), ValueError(f'To search tags, you must provide a list, tuple, or set. You provided {type(tags)}')

    v_method_dict = {}
    for tag in tags:
        v_method_dict.update(search_tag(obj, tag))
    return v_method_dict

def get_first_tag(obj: Dict[str, Callable], tag: str) -> str:
    return list(search_tag(obj, tag).keys())[0]