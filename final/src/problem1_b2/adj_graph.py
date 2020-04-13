import numpy as np
from pathlib import Path
from graphviz import Digraph
# import ..settings


def draw_adj_graph(arcs, filename: str, output_dir: Path):

    g = Digraph('G',
                filename=filename,
                directory=output_dir,
                format='pdf')
    g.attr(rankdir='LR')

    for i in range(len(arcs) - 1):
        for j in range(len(arcs[i])):
            if arcs[i][j]:
                g.edge(str(j + 1), str(i + 1))

    for j in range(len(arcs[-1])):
        if arcs[-1][j]:
            g.edge(str(j + 1), 'Done')

    g.render()
