import math
import statistics

def calculate(xs):
    """Standardized third moment."""
    if len(xs)<3: return 0.0
    m=statistics.mean(xs); s=statistics.pstdev(xs)
    return sum(((x-m)/s)**3 for x in xs)/len(xs) if s else 0.0
