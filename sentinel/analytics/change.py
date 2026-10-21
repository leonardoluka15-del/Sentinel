import math
import statistics

def calculate(xs):
    """Latest first difference."""
    return xs[-1]-xs[-2] if len(xs)>1 else 0.0
