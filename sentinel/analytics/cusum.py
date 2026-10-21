import math
import statistics

def calculate(xs):
    """One-sided cumulative sum with 0.5 standard deviation drift."""
    if len(xs)<4: return 0.0
    b=xs[:max(3,len(xs)//2)]; m=statistics.mean(b); s=max(statistics.pstdev(b),0.001); c=0
    for x in xs[len(b):]: c=max(0,c+(x-m)/s-0.5)
    return c
