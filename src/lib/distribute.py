import numpy as np


def split_into_processors(N: int, N_p: int) -> np.array:
    if N_p <= 0:
        raise Exception('N_p must be non-zero')
    if N_p > N:
        return np.arange(N)

    points_per_processor = N // N_p
    mapping = np.zeros(N, dtype=int)
    for index in range(N):
        processor = min(index // points_per_processor, N_p - 1)
        mapping[index] = processor
    return mapping
