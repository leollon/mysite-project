"""Prime a generator
"""
from functools import wraps


def primer_generator(func):
    """Decorator: primes `func` by advancing first `yield`"""
    @wraps(func)
    def primer(*args, **kwargs):
        generator = func(*args, **kwargs)  # get an generator object
        next(generator)  # prime the generator
        return generator
    return primer
