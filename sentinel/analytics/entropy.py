import math
import statistics

def calculate(xs):
    """Shannon entropy over ten equal-width bins."""
    if not xs or max(xs)==min(xs): return 0.0
    lo=min(xs); span=max(xs)-lo; bins=[0]*10
    for x in xs: bins[min(9,int(10*(x-lo)/span))]+=1
    return -sum((n/len(xs))*math.log2(n/len(xs)) for n in bins if n)
