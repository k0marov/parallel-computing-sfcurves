import numpy as np
from matplotlib.collections import LineCollection
import matplotlib.pyplot as plt


def plot_mapping(N, M, curve, proc_map_2d, save_as: str):
    assert N*M == len(curve)
    segments = np.array([curve[:-1], curve[1:]]).transpose(1, 0, 2)

    segment_values = proc_map_2d[1:]

    cmap = plt.get_cmap('rainbow')

    plt.figure(figsize=(7, 7))
    norm = plt.Normalize(vmin=proc_map_2d.min(), vmax=proc_map_2d.max())
    segment_colors = cmap(norm(segment_values))

    lc = LineCollection(segments, colors=segment_colors)

    fig, ax = plt.subplots()
    ax.add_collection(lc)

    ax.set_xlim(-1, N)
    ax.set_xticks(range(0, N + 1, 2 if N < 32 else 8))
    ax.set_yticks(range(0, M + 1, 2 if M < 32 else 8))
    ax.set_ylim(-1, M)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.savefig(save_as)

