import math
import statistics

def calculate(xs):
    """Fraction of rising transitions."""
    return sum(b>a for a,b in zip(xs,xs[1:]))/max(1,len(xs)-1)
