import math
import sys

import numpy as np

from lib import distribute
from lib import curves
from lib.misc import draw
from lib.misc import export


def pipeline(N, M, N_p):
    curve, xy_to_index = curves.generate_hilbert_mappings(N, M)
    assert(len(curve) == N*M)

    proc_map = distribute.split_into_processors(N * M, N_p)
    proc_2d_arr = np.take(proc_map, xy_to_index)
    return curve, proc_map, proc_2d_arr

def main(N, M, N_p):
    curve, proc_map_2d, proc_2d_arr = pipeline(N, M, N_p)

    csv_path = f"output/hilbert_{N}x{M}_into_{N_p}.csv"
    export.save_array(proc_2d_arr, csv_path)
    print(f"Saved mapping into '{csv_path}'")

    if N > 256:
        return

    img_path = f"output/hilbert_{N}x{M}_into_{N_p}.png"
    draw.plot_mapping(N, M, curve, proc_map_2d, save_as=img_path)
    print(f"Saved image into '{img_path}'")

if __name__ == '__main__':
    if len(sys.argv) == 3:
        N = int(sys.argv[1])
        M = int(sys.argv[2])
        N_p = int(sys.argv[3])
        print(f"Running with N = {N}, M = {M} and N_p = {N_p}")
    else:
        N = int(input("Side 1 of the rectangle, N = "))
        M = int(input("Side 2 of the rectangle, M = "))
        N_p = int(input("Number of processors, N_p = "))
    main(N, M, N_p)