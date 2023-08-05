"""Main module."""
import pandas as pd
import numpy as np


def sqrt_function(num):
    return np.sqrt(num)

def say_hello(name=None):
    if name is None:
        return 'Hello, Mehul here...'
    else:
        return f'Hello, {name}!'

