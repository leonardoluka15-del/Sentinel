import math
import statistics

def calculate(xs):
    """Fraction of samples exceeding 85 percent."""
    return sum(x>85 for x in xs)/len(xs) if xs else 0.0
