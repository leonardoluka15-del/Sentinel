import math
import statistics

def calculate(xs):
    """Root mean square magnitude."""
    return math.sqrt(sum(x*x for x in xs)/len(xs)) if xs else 0.0
