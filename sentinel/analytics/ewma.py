import math
import statistics

def calculate(xs):
    """Exponentially weighted current level, alpha 0.25."""
    if not xs: return 0.0
    v=xs[0]
    for x in xs[1:]: v=0.25*x+0.75*v
    return v
