import math
import statistics

def calculate(xs):
    """Walk-forward persistence mean absolute error."""
    return sum(abs(b-a) for a,b in zip(xs,xs[1:]))/max(1,len(xs)-1)
