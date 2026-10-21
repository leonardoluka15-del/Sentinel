import math
import statistics

def calculate(xs):
    """Linearly interpolated 95th percentile."""
    if not xs: return 0.0
    s = sorted(xs); i = (len(s)-1)*0.95; lo = int(i)
    return s[lo] + (s[min(lo+1,len(s)-1)]-s[lo])*(i-lo)
