import math
import statistics

def calculate(xs):
    """Lag-one autocorrelation."""
    if len(xs)<3: return 0.0
    a=xs[:-1]; b=xs[1:]; ma=statistics.mean(a); mb=statistics.mean(b)
    den=math.sqrt(sum((x-ma)**2 for x in a)*sum((x-mb)**2 for x in b))
    return sum((x-ma)*(y-mb) for x,y in zip(a,b))/den if den else 0.0
