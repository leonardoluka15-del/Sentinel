import math
import statistics

def calculate(xs):
    """Median robust location estimate."""
    return statistics.median(xs) if xs else 0.0
