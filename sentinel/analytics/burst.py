import math
import statistics

def calculate(xs):
    """Peak to median ratio."""
    return max(xs)/max(abs(statistics.median(xs)),0.001) if xs else 0.0
