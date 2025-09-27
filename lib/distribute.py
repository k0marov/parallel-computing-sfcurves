import numpy as np

def split_into_processors(N: int, N_p: int) -> np.array:
    if N_p <= 0:
        raise Exception('N_p must be non-zero')
    if N_p > N:
        return np.arange(N)

    base_points = N // N_p
    remainder = N % N_p
    
    indices = np.arange(N)
    
    threshold = remainder * (base_points + 1)
    processor = np.where(
        indices < threshold,
        indices // (base_points + 1),
        remainder + (indices - threshold) // base_points
    )
    
    return processor
