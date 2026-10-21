import math
import statistics

def calculate(xs):
    """Excess fourth standardized moment."""
    if len(xs)<4: return 0.0
    m=statistics.mean(xs); s=statistics.pstdev(xs)
    return sum(((x-m)/s)**4 for x in xs)/len(xs)-3 if s else 0.0
