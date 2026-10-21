import math
import statistics

def calculate(xs):
    """Linear extrapolation six samples ahead."""
    if len(xs)<2: return xs[-1] if xs else 0.0
    n=len(xs); t=(n-1)/2; m=statistics.mean(xs)
    s=sum((i-t)*(x-m) for i,x in enumerate(xs))/sum((i-t)**2 for i in range(n))
    return m+s*((n-1)+6-t)
