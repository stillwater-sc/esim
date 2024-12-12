import numpy as np

def randomizer(value: float, lowerbound: float = 0.0, upperbound: float = 0.0) -> float:
    """generates a uniform random value derived from the range defined by [lowerbound, upperbound]*value

    randomizer generates a uniform random value.
    lowerbound and upperbound are specified as proportions to the
    input value and thus should be in the range [0, 1]

    Args: 
        value (float): the value to be randomized
        lowerbound (float): the lower bound of the range
        upperbound (float): the upper bound of the range

    Returns:
        uniformly randomized value (float)
    """
    diff = upperbound - lowerbound
    if diff < 0.01:
        return value

    # generate a randomized value in the range
    low: float = lowerbound * value
    high: float = upperbound * value
    sample: float = np.random.uniform(low, high)
    return sample