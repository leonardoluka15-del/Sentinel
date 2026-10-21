import math
import statistics

def calculate(xs):
    """Latest robust z-score against earlier observations."""
    if len(xs)<4: return 0.0
    b=xs[:-1]; m=statistics.median(b); d=statistics.median(abs(x-m) for x in b)
    return 0.6745*(xs[-1]-m)/max(d,0.001)
