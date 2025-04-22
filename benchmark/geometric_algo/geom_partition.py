import math
import numpy as np
from typing import List, Tuple


class Tile:
    def __init__(self, i_s: int = 0, i_e: int = 0, j_s: int = 0, j_e: int = 0):
        self.i_s = i_s
        self.i_e = i_e
        self.j_s = j_s
        self.j_e = j_e


class Partition:
    def __init__(self):
        self.proc_map = None
        self.panel_map = None
        self.tiles = None


def gcd(a: int, b: int) -> int:
    """Returns the greatest common divisor of a and b"""
    if a == 0 or b == 0:
        return max(a, b)
    return gcd(b, a % b)


def gcd_array(array: List[int]) -> int:
    """Returns the GCD of an array of integers"""
    divisor = array[0]
    for num in array[1:]:
        divisor = gcd(divisor, num)
        if divisor == 1:
            break
    return divisor


def lcm(a: int, b: int) -> int:
    """Returns the least common multiple of a and b"""
    return a * b // gcd(a, b)


def partition_1d(Np: int, N: int) -> Tuple[np.ndarray, np.ndarray]:
    """Partitions a 1D range into Np parts"""
    mean_work = N // Np
    work = np.full(Np, mean_work, dtype=int)
    deficite = N % Np
    work[:deficite] += 1

    i_s = np.zeros(Np, dtype=int)
    i_e = np.zeros(Np, dtype=int)

    i_s[0] = 1
    i_e[0] = work[0]
    for i in range(1, Np):
        i_s[i] = i_e[i - 1] + 1
        i_e[i] = i_e[i - 1] + work[i]

    return i_s, i_e


def get_closest_factors(n: int) -> List[int]:
    """Returns two factors of n that are closest to each other"""
    f1 = int(math.sqrt(n))
    while True:
        if n % f1 == 0:
            break
        f1 -= 1
    return [n // f1, f1]


def create_partition(npanels: int, Nx: List[int], Ny: List[int], nprocs: int) -> Partition:
    """
    Creates a partition of panels into tiles and distributes them across processes

    Args:
        npanels: total number of panels to partition
        Nx: number of points along x dimension at each panel
        Ny: number of points along y dimension at each panel
        nprocs: total number of processes

    Returns:
        Partition object containing the mapping of tiles to panels and processes
    """
    partition = Partition()
    panel_weight = np.zeros(npanels, dtype=int)

    for ipanel in range(npanels):
        panel_weight[ipanel] = Nx[ipanel] * Ny[ipanel]

    # Determine minimum number of tiles needed for equal distribution
    # of grid points across these tiles
    min_tiles_num = sum(panel_weight) // gcd_array(list(panel_weight) + [sum(panel_weight)])

    N_tiles = (lcm(nprocs, min_tiles_num) * panel_weight) // sum(panel_weight)
    Nt = sum(N_tiles)  # total number of tiles

    partition.proc_map = np.zeros(Nt, dtype=int)
    partition.panel_map = np.zeros(Nt, dtype=int)
    tmp_tiles = [Tile() for _ in range(Nt)]

    itile = 0
    for ipanel in range(npanels):
        # Panel partition block
        ntx_nty = get_closest_factors(N_tiles[ipanel])
        ntx, nty = ntx_nty[0], ntx_nty[1]

        i_s, i_e = partition_1d(ntx, Nx[ipanel])
        j_s, j_e = partition_1d(nty, Ny[ipanel])

        for iy in range(nty):
            for ix in range(ntx):
                partition.panel_map[itile] = ipanel + 1  # +1 for 1-based indexing
                tmp_tiles[itile].i_s = i_s[ix]
                tmp_tiles[itile].i_e = i_e[ix]
                tmp_tiles[itile].j_s = j_s[iy]
                tmp_tiles[itile].j_e = j_e[iy]
                itile += 1

    # Distribute tiles block
    ts_global, te_global = partition_1d(nprocs, Nt)

    for ip in range(nprocs):
        for itile in range(ts_global[ip] - 1, te_global[ip]):  # -1 for 0-based indexing
            partition.proc_map[itile] = ip

    partition.tiles = tmp_tiles
    return partition
