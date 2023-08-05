from typing import Callable

def no_raise(func: Callable):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper

def suppress_raise(func: Callable):
    def wrapper(*args, **kwargs):
        try:
           return func(*args, **kwargs)
        except:
            return None

    return wrapper

def raises(func: Callable):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except:
            raise

    return wrapper