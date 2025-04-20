import matplotlib.pyplot as plt
import numpy as np

from lib import distribute, curves
from benchmark import perimeter_sum


def pipeline(N, M, N_p):
    curve, xy_to_index = curves.generate_hilbert_mappings(N, M)
    assert(len(curve) == N*M)

    proc_map = distribute.split_into_processors(N * M, N_p)
    proc_2d_arr = np.take(proc_map, xy_to_index)
    return curve, proc_map, proc_2d_arr

def plot_perimeter_sum(N_p, max_N):
    X = list(range(10, max_N))
    Y = [perimeter_sum.calculate_total_perimeter(pipeline(n, n, N_p)[2]) for n in X]
    plt.plot(X, Y)
    plt.title("Зависимость суммарного периметра в NxN на N_p = 30 от N")
    plt.xlabel("N")
    plt.ylabel("Perimeter sum")
    plt.savefig("benchmark.png")
    plt.show()

if __name__ == '__main__':
    plot_perimeter_sum(30, 100)
