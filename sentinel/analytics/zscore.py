import math
import statistics

def calculate(xs):
    """Latest observation z-score against previous baseline."""
    if len(xs)<4: return 0.0
    b=xs[:-1]; s=statistics.pstdev(b)
    return (xs[-1]-statistics.mean(b))/max(s,0.001)
