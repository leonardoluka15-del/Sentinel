import math
import statistics

def calculate(xs):
    """Coefficient of variation."""
    return statistics.pstdev(xs)/max(abs(statistics.mean(xs)),0.001) if xs else 0.0
