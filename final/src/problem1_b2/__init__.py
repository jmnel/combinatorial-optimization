import settings
from . import model_params
from .task import Task
from pprint import pprint
from .adj_graph import draw_adj_graph

pprint(Task.all()[-1].predecessors)

arcs = [[1 if p in t.predecessors else 0 for p in range(len(Task.all()))]
        for t in Task.all()]

draw_adj_graph(arcs,
               filename='fig1-1',
               output_dir=settings.project_fig_dir)
