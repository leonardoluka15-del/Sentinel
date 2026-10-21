import math
import statistics

def calculate(xs):
    """Latest second difference."""
    return xs[-1]-2*xs[-2]+xs[-3] if len(xs)>2 else 0.0
