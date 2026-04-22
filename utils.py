import math


def mean(values):
    return sum(values) / len(values) if values else 0


def std_dev(values):
    if len(values) < 2:
        return 1.0
    avg = mean(values)
    variance = sum((x - avg) ** 2 for x in values) / len(values)
    return math.sqrt(variance)
