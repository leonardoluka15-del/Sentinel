import math
import statistics

def calculate(xs):
    """Arithmetic average."""
    return sum(xs) / len(xs) if xs else 0.0
