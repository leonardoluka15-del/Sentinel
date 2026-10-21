import math
import statistics

def calculate(xs):
    """Population variance."""
    m = sum(xs)/len(xs) if xs else 0
    return sum((x-m)**2 for x in xs)/len(xs) if xs else 0.0
