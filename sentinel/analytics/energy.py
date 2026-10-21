import math
import statistics

def calculate(xs):
    """Sum of squared samples."""
    return sum(x*x for x in xs)
