import math
import statistics

def calculate(xs):
    """Median absolute deviation."""
    if not xs: return 0.0
    m=statistics.median(xs)
    return statistics.median(abs(x-m) for x in xs)
