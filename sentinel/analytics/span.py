import math
import statistics

def calculate(xs):
    """Observed dynamic range."""
    return max(xs)-min(xs) if xs else 0.0
