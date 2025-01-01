import math


def ease_in_out_circ(x: float) -> float:
    if x < 0.5:
        return (1 - math.sqrt(1 - (2 * x) ** 2)) / 2
    else:
        return (math.sqrt(1 - (2 * x - 2) ** 2) + 1) / 2
