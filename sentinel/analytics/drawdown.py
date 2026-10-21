import math
import statistics

def calculate(xs):
    """Largest decline from a preceding maximum."""
    peak=0; worst=0
    for x in xs: peak=max(peak,x); worst=max(worst,peak-x)
    return worst
