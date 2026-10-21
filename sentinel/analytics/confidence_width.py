import math
import statistics

def calculate(xs):
    """Approximate 95 percent interval for sample mean; IID assumption."""
    return 1.96*statistics.pstdev(xs)/math.sqrt(len(xs)) if xs else 0.0
