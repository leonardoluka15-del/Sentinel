import math
import statistics

def calculate(xs):
    """Least squares slope per sample."""
    n=len(xs)
    if n<2: return 0.0
    t=(n-1)/2; m=sum(xs)/n
    return sum((i-t)*(x-m) for i,x in enumerate(xs))/sum((i-t)**2 for i in range(n))
