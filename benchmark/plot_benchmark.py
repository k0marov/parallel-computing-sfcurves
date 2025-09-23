import statistics
import matplotlib.pyplot as plt
import numpy as np

from lib import distribute, curves
from benchmark import metrics
from benchmark.geometric_algo import geom_partition


def pipeline(N, M, N_p):
    curve, xy_to_index = curves.generate_hilbert_mappings(N, M)
    assert(len(curve) == N*M)

    proc_map = distribute.split_into_processors(N * M, N_p)
    proc_2d_arr = np.take(proc_map, xy_to_index)
    return curve, proc_map, proc_2d_arr

def geom_pipeline(N, M, N_p):
    result = geom_partition.create_partition(1, [N], [M], N_p)
    return geom_partition.partition_to_2d_arrays(result, [N], [M])[0]
    # perimeter_sum = sum([2*(abs(t.i_s - t.i_e)+1 + abs(t.j_s - t.j_e)+1) for t in result.tiles])
    # return perimeter_sum


def plot_perimeter_sum(N, max_N_p):
    X = list(range(10, max_N_p))
    Y = [statistics.mean(metrics.get_perimeters(geom_pipeline(N, N, n_p))) for n_p in X]
    print(max(Y))
    plt.plot(X, Y, label='Геометрический алгоритм')
    Y = [statistics.mean(metrics.get_perimeters(pipeline(N, N, n_p)[2])) for n_p in X]
    print(max(Y))
    plt.plot(X, Y, label='Разбиение через кривые Гилберта')
    plt.title(f"Зависимость среднего периметра в NxN, где N={N} от N_p")
    plt.xlabel("N_p")
    plt.ylabel("Mean perimeter")
    plt.legend()
    plt.savefig("benchmark.png")
    plt.show()

if __name__ == '__main__':
    plot_perimeter_sum(100, 200)
