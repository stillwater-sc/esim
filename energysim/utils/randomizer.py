import numpy as np

# generate a randomized sample. lowerbound and upperbound are specified as proportions to the
# input value and thus should be in the range [0, 1]
def randomizer(value: float, lowerbound: float = 0.0, upperbound: float = 0.0) -> float:
    diff = upperbound - lowerbound
    if diff < 0.01:
        return value

    # generate a randomized value in the range
    low: float = lowerbound * value
    high: float = upperbound * value
    sample: float = np.random.uniform(low, high)
    return sample